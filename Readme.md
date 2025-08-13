<h1 align="center">
&#11088; <code>GitStarPercentile</code>
</h1>

<div align="center">

[![Twitter](https://img.shields.io/twitter/follow/ChenLiu-1996.svg?style=social)](https://twitter.com/ChenLiu_1996)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ChenLiu-1996?color=blue)](https://www.linkedin.com/in/chenliu1996/)
<br>
[![Latest PyPI version](https://img.shields.io/pypi/v/git-star-percentile.svg)](https://pypi.org/project/git-star-percentile/)
[![PyPI download 3 month](https://static.pepy.tech/badge/git-star-percentile)](https://pepy.tech/projects/git-star-percentile)
[![PyPI download month](https://img.shields.io/pypi/dm/git-star-percentile.svg)](https://pypistats.org/packages/git-star-percentile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

<br>
Have you ever wondered how popular your GitHub repository really is?

Frustrated that GitHub doesn’t show where your star count ranks among all public repos?

Maybe you’ve thought: "I have 200 stars — but is that a lot?" or "Where does my repo rank compared to the rest?"

<br>
<code>GitStarPercentile</code> tells you instantly:

    Enter your star count and instantly see your percentile, calculated from GitHub-wide data.


## &#128640; Features

- &#128202; **Instant percentile lookup** — get your repo’s rank in seconds.
- &#128421; **Simple CLI** — just type `git-star-percentile` and enter your star count.


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

```bash
Enter the number of GitHub stars: 250
Your repository is in the top 3.7% of all public GitHub repositories.
```

## &#128196; Data Source

- Star statistics are **pulled from all public GitHub repositories**.
- Data is stored in [stats/github_repo_stars.csv](stats/github_repo_stars.csv).
- Want fresher stats? Run [the stats counter](count_all_repo_stars.py) yourself and submit a pull request.
