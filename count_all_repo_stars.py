#!/usr/bin/env python3
import os, sys, csv, time, argparse
from datetime import datetime
import requests
from tqdm import tqdm

REST_API   = "https://api.github.com/repositories"
GQL_API    = "https://api.github.com/graphql"
SEARCH_API = "https://api.github.com/search/repositories"

GQL_QUERY = """
query($ids:[ID!]!){
  nodes(ids:$ids){
    __typename
    ... on Repository{
      id
      nameWithOwner
      stargazerCount
      isFork
      isArchived
      isPrivate
      createdAt
      pushedAt
      primaryLanguage{ name }
      databaseId
    }
  }
}
"""

def session_with_token(tok: str) -> requests.Session:
    if not tok:
        print("ERROR: --github-token is required.", file=sys.stderr); sys.exit(1)
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-star-crawler/PROGBAR-ID-STRATIFIED-RESUME",
        "Authorization": f"Bearer {tok}",
    })
    return s

def backoff_on_limit(resp: requests.Response):
    if resp.status_code != 403:
        return
    reset = resp.headers.get("X-RateLimit-Reset")
    retry_after = resp.headers.get("Retry-After")
    if retry_after:
        time.sleep(int(retry_after)); return
    if reset:
        wait = max(0, int(reset) - int(time.time())) + 1
        time.sleep(wait); return
    time.sleep(10)

def write_header_if_needed(path: str):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "repo_id","node_id","full_name","stargazers_count",
                "fork","archived","private","created_at","pushed_at","language"
            ])

def load_state(state_path: str):
    if os.path.exists(state_path):
        try:
            bucket_str, repo_str = open(state_path, "r", encoding="utf-8").read().strip().split(",")
            return int(bucket_str), int(repo_str)
        except Exception:
            pass
    return 0, 0

def save_state(state_path: str, bucket_idx: int, repo_id: int):
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(f"{bucket_idx},{repo_id}")

def _page_after(session: requests.Session, since_id: int, per_page: int = 1, timeout: int = 20) -> bool:
    try:
        r = session.get(REST_API, params={"since": since_id, "per_page": per_page}, timeout=timeout)
    except requests.RequestException:
        return False
    if r.status_code != 200:
        return False
    return bool(r.json())

def find_max_public_repo_id(session: requests.Session, start_hint: int = 1_000_000_000) -> int:
    low, high = 0, max(1, start_hint)
    while _page_after(session, high):
        low, high = high, high * 2
        time.sleep(0.03)
    while low + 1 < high:
        mid = (low + high) // 2
        if _page_after(session, mid):
            low = mid
        else:
            high = mid
    return high - 1

def estimate_total_via_search(session: requests.Session) -> int:
    try:
        r = session.get(SEARCH_API, params={"q": "is:public", "per_page": 1}, timeout=30)
        if r.status_code != 200:
            return 0
        return int(r.json().get("total_count", 0))
    except Exception:
        return 0

def gql_nodes(session: requests.Session, ids: list[str]) -> list[dict]:
    try:
        r = session.post(GQL_API, json={"query": GQL_QUERY, "variables": {"ids": ids}}, timeout=60)
        if r.status_code != 200:
            return []
        data = r.json()
        return data.get("data", {}).get("nodes", [])
    except Exception:
        return []

def process_repos(sess, repos, buf, w, gql_batch, total_written):
    page_max_id = max((r.get("id") for r in repos if isinstance(r.get("id"), int)), default=0)
    for repo in repos:
        buf.append((repo.get("node_id"), repo.get("id"), repo.get("full_name")))
        if len(buf) >= gql_batch:
            nodes = gql_nodes(sess, [x[0] for x in buf])
            wrote = 0
            for node, (_, dbid, fallback_name) in zip(nodes, buf):
                if node and node.get("__typename") == "Repository":
                    w.writerow([
                        node.get("databaseId") or dbid,
                        node.get("id"),
                        node.get("nameWithOwner") or fallback_name,
                        node.get("stargazerCount"),
                        node.get("isFork"),
                        node.get("isArchived"),
                        node.get("isPrivate"),
                        node.get("createdAt"),
                        node.get("pushedAt"),
                        (node.get("primaryLanguage") or {}).get("name"),
                    ])
                    wrote += 1
            total_written += wrote
            buf.clear()
    return page_max_id, total_written

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-token", type=str, required=True)
    ap.add_argument("--out", default="./stats/github_repo_stars.csv")
    ap.add_argument("--state", default="./stats/state_last_repo_id.txt")
    ap.add_argument("--per-page", type=int, default=100)
    ap.add_argument("--gql-batch", type=int, default=100)
    ap.add_argument("--rest-sleep", type=float, default=0.05)
    ap.add_argument("--gql-sleep", type=float, default=0.0)
    ap.add_argument("--sample-size", type=int, default=None, help="Number of repos to sample; None for all repos")
    ap.add_argument("--num-buckets", type=int, default=100, help="Number of buckets for stratified sampling")
    args = ap.parse_args()

    sess = session_with_token(args.github_token)
    write_header_if_needed(args.out)
    start_bucket, since = load_state(args.state)
    print(f"[START] Resuming from bucket {start_bucket}, repo_id > {since} at {datetime.now().isoformat(timespec='seconds')}")

    print("[INFO] Probing current max public repo id...", flush=True)
    if since > 0:
        # Add a small buffer (5%) to the last seen ID, but at least +10,000
        hint = since + max(10_000, int(since * 0.05))
    else:
        # First run: start at a reasonable mid‐range ID instead of a giant number
        hint = 500_000_000
    max_pub_id = find_max_public_repo_id(sess, start_hint=hint)
    search_total = estimate_total_via_search(sess)

    pbar = tqdm(total=max_pub_id, unit="id", dynamic_ncols=True, initial=since)
    pbar.set_description(f"Latest GitHub Repo ID (max ID = {max_pub_id:,}) | roughly {search_total:,} public repos.")

    total_written = 0
    buf = []

    with open(args.out, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        if args.sample_size is None:
            bucket_range = [(0, since, max_pub_id)]
        else:
            bucket_size = max_pub_id // args.num_buckets
            quota_per_bucket = max(1, args.sample_size // args.num_buckets)
            bucket_range = []
            for b in range(start_bucket, args.num_buckets):
                start_id = b * bucket_size
                if b == start_bucket:
                    start_id = since
                end_id = (b + 1) * bucket_size
                bucket_range.append((b, start_id, end_id, quota_per_bucket))

        if args.sample_size is None:
            b_idx, start_id, end_id = bucket_range[0]
            since = start_id
            while since < end_id:
                try:
                    r = sess.get(REST_API, params={"since": since, "per_page": args.per_page}, timeout=30)
                    if r.status_code != 200:
                        break
                except Exception:
                    break
                repos = r.json()
                if not repos:
                    break
                page_max_id, total_written = process_repos(sess, repos, buf, w, args.gql_batch, total_written)
                since = page_max_id
                pbar.n = since
                pbar.set_postfix(written=total_written)
                pbar.refresh()
                save_state(args.state, 0, since)
                time.sleep(args.rest_sleep)
        else:
            for b_idx, start_id, end_id, quota in bucket_range:
                bucket_written = 0
                since = start_id
                while since < end_id and bucket_written < quota:
                    try:
                        r = sess.get(REST_API, params={"since": since, "per_page": args.per_page}, timeout=30)
                        if r.status_code != 200:
                            break
                    except Exception:
                        break
                    repos = r.json()
                    if not repos:
                        break
                    page_max_id, total_written = process_repos(sess, repos, buf, w, args.gql_batch, total_written)
                    bucket_written += len(repos)
                    since = page_max_id
                    pbar.n = since
                    pbar.set_postfix(written=total_written)
                    pbar.refresh()
                    save_state(args.state, b_idx, since)
                    if total_written >= args.sample_size:
                        break
                    time.sleep(args.rest_sleep)
                if total_written >= args.sample_size:
                    break

    pbar.close()
    print(f"[DONE] Wrote {total_written:,} repos to {args.out}")

if __name__ == "__main__":
    main()
