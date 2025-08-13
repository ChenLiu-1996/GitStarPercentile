import pandas as pd
import requests
import os

CSV_URL = "https://raw.githubusercontent.com/ChenLiu-1996/GitStarPercentile/main/stats/github_repo_stars.csv"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".git_star_percentile")
CACHE_FILE = os.path.join(CACHE_DIR, "github_repo_stars.csv")

def load_csv():
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.exists(CACHE_FILE):
        print("Downloading star statistics...")
        r = requests.get(CSV_URL)
        r.raise_for_status()
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(r.text)
    return pd.read_csv(CACHE_FILE, usecols=["stargazers_count"])

def main():
    try:
        stars = int(input("Enter your GitHub repo star count: ").strip())
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    df = load_csv()
    star_counts = df["stargazers_count"].dropna().astype(int)
    total = len(star_counts)
    rank = (star_counts <= stars).sum()
    percentile = 100 * rank / total

    print(f"Your repo is approximately at the {percentile:.2f} percentile.")
    print(f"({rank:,} out of {total:,} repos have ≤ this many stars.)")

if __name__ == "__main__":
    main()
