<h1 align="center">
&#x2B50; <code>GitStarPercentile</code>
</h1>

<div align="center">

[![Twitter](https://img.shields.io/twitter/follow/ChenLiu-1996.svg?style=social)](https://twitter.com/ChenLiu_1996)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ChenLiu-1996?color=blue)](https://www.linkedin.com/in/chenliu1996/)
<br>
[![Latest PyPI version](https://img.shields.io/pypi/v/citation-map.svg)](https://pypi.org/project/citation-map/)
[![PyPI download 3 month](https://static.pepy.tech/badge/citation-map)](https://pepy.tech/projects/citation-map)
[![PyPI download month](https://img.shields.io/pypi/dm/citation-map.svg)](https://pypistats.org/packages/citation-map)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>


---

Have you ever wondered **how popular your GitHub repository really is**?

Ever felt frustrated that GitHub doesn’t show where your star count ranks among *all* public repos?

Have you found yourself thinking:
> *"I have 200 stars — but is that a lot?"*
> *"Where does my repo rank compared to the rest of GitHub repos?"*

**GitStarPercentile** tells you instantly. Just type your star count, and it calculates your percentile based on the latest GitHub-wide statistics.

---

## Features

- 📊 **Instant percentile lookup** for any GitHub repo star count.
- 🖥️ **Simple CLI** — just type `git-star-percentile` and enter your star count.

---

## &#128230; Installation

From the command line:

```bash
    pip install git-star-percentile --upgrade
```

## &#9889; Usage
From the command line:

```bash
    git-star-percentile
```

You’ll be prompted to enter the number of stars for your repository:

    Enter the number of GitHub stars: 250
    Your repository is in the top 3.7% of all public GitHub repositories.

## &#128196; Data Source

- Star statistics are **read directly from GitHub’s public repositories**.
- The dataset is stored in [stats/github_repo_stars.csv](stats/github_repo_stars.csv).
- If you have the spare time to run an updated version, create a pull request so that we can get the latest numbers.
