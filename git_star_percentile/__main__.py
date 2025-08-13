import os
import pandas as pd
import requests

CSV_URL = "https://raw.githubusercontent.com/ChenLiu-1996/GitStarPercentile/main/stats/github_repo_stars.csv"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".git_star_percentile")
CACHE_FILE = os.path.join(CACHE_DIR, "github_repo_stars.csv")


def load_csv() -> pd.DataFrame:
    os.makedirs(CACHE_DIR, exist_ok=True)

    try:
        r = requests.get(CSV_URL, timeout=30)
        r.raise_for_status()
        with open(CACHE_FILE, "wb") as f:
            f.write(r.content)
        print("Downloading latest CSV from remote...")
    except requests.RequestException as e:
        if os.path.exists(CACHE_FILE):
            print(f"Network error ({e}). Using cached CSV: {CACHE_FILE}")
        else:
            # No cache to fall back on
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
    rank = (curr_stars <= star_counts).sum()  # repos with at least this many stars
    percentile = 100 * rank / total

    print(f"Your repo is approximately among the top {percentile:.4f}%.")
    print(f"({rank:,} out of {total:,} repos have at least this many stars.)")

if __name__ == "__main__":
    main()
