import os
import json
import pandas as pd
import requests

CSV_URL = "https://raw.githubusercontent.com/ChenLiu-1996/GitStarPercentile/main/stats/github_repo_stars.csv"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".git_star_percentile")
CACHE_FILE = os.path.join(CACHE_DIR, "github_repo_stars.csv")
META_FILE  = os.path.join(CACHE_DIR, "metadata.json")

def _read_meta():
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_meta(meta: dict):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f)

def _conditional_headers(meta: dict):
    h = {}
    etag = meta.get("etag")
    lm   = meta.get("last_modified")
    if etag:
        h["If-None-Match"] = etag
    if lm:
        h["If-Modified-Since"] = lm
    return h

def load_csv():
    os.makedirs(CACHE_DIR, exist_ok=True)

    meta = _read_meta()
    headers = _conditional_headers(meta)

    try:
        # Conditional GET to avoid redownloading if unchanged
        r = requests.get(CSV_URL, headers=headers, timeout=30)
        if r.status_code == 304 and os.path.exists(CACHE_FILE):
            # Not modified; use cache
            pass
        elif r.ok:
            # Updated or first time: write new bytes, then update metadata
            with open(CACHE_FILE, "wb") as f:
                f.write(r.content)
            new_meta = {
                "etag": r.headers.get("ETag"),
                "last_modified": r.headers.get("Last-Modified"),
                "content_length": r.headers.get("Content-Length"),
                "url": CSV_URL,
            }
            _write_meta(new_meta)
        else:
            # If we have a cache, fall back to it; otherwise raise
            if not os.path.exists(CACHE_FILE):
                r.raise_for_status()
            # else: silently use the cache
    except requests.RequestException:
        # Network issue: if no cache, re-raise; else use cache
        if not os.path.exists(CACHE_FILE):
            raise

    # Now load the CSV (header is present per your crawler)
    return pd.read_csv(CACHE_FILE, usecols=["stargazers_count"])

def main():
    try:
        curr_stars = int(input("Enter your GitHub repo star count: ").strip())
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    df = load_csv()
    star_counts = df["stargazers_count"].dropna().astype(int)
    total = len(star_counts)
    rank = (curr_stars <= star_counts).sum()
    percentile = 100 * rank / total

    print(f"Your repo is approximately among the top {percentile:.4f}%.")
    print(f"({rank:,} out of {total:,} repos have at least this many stars.)")

if __name__ == "__main__":
    main()
