import os
import json
import time
import pandas as pd
import requests
from urllib.parse import urlencode

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
    # Revalidate at origin (don’t serve from CDN cache without checking)
    h["Cache-Control"] = "no-cache"
    h["Pragma"] = "no-cache"
    return h

def _maybe_cache_busted_url(url: str) -> str:
    # Force refresh if env var is set, e.g. GSP_FORCE_REFRESH=1
    if os.getenv("GSP_FORCE_REFRESH") in ("1", "true", "True"):
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}{urlencode({'_': int(time.time())})}"
    return url

def load_csv():
    os.makedirs(CACHE_DIR, exist_ok=True)

    meta = _read_meta()
    headers = _conditional_headers(meta)
    url = _maybe_cache_busted_url(CSV_URL)

    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 304 and os.path.exists(CACHE_FILE):
            # If CDN is slow to update and you *know* there’s a new file,
            # allow a one-shot retry with a cache-busting URL.
            if not os.getenv("GSP_FORCE_REFRESH"):
                # Retry once with a cache-buster
                busted = _maybe_cache_busted_url(CSV_URL + ("&retry=1" if "?" in CSV_URL else "?retry=1"))
                r2 = requests.get(busted, headers=headers, timeout=30)
                if r2.ok and r2.content:
                    with open(CACHE_FILE, "wb") as f:
                        f.write(r2.content)
                    new_meta = {
                        "etag": r2.headers.get("ETag"),
                        "last_modified": r2.headers.get("Last-Modified"),
                        "content_length": r2.headers.get("Content-Length"),
                        "url": CSV_URL,
                    }
                    _write_meta(new_meta)
                # else fall through to cached file
            # else: user explicitly wants to force refresh; _maybe_cache_busted_url already handled it
            pass
        elif r.ok:
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
            if not os.path.exists(CACHE_FILE):
                r.raise_for_status()
            # else: silently use the cache
    except requests.RequestException:
        if not os.path.exists(CACHE_FILE):
            raise

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
