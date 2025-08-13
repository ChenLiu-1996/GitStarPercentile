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

&#129300; Have you ever wondered **how popular your GitHub repository really is**?

&#x1F620; Frustrated that GitHub **doesn’t show star percentiles anywhere**?

Maybe you’ve thought:
> "I have 200 stars — but is that a lot?"

> "Where does my repo rank compared to the other repos?"

<br>
<code>GitStarPercentile</code> tells you instantly:

Enter your star count and instantly see your percentile, calculated from GitHub-wide data.


## &#128640; Features

- &#128202; **Instant percentile lookup** — get your repo’s rank in milliseconds.
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
Enter the number of GitHub stars: 200
Your repo is approximately among the top 0.4421%.
```

## &#128196; Data Source

<img src="assets/github_stars_distribution.png" alt="GitHub Stars Distribution" style="max-width:100%; height:auto;">>

- Star statistics are **pulled from all public GitHub repositories**.
- Data is stored in [stats/github_repo_stars.csv](stats/github_repo_stars.csv).
- Want fresher stats? Run [the stats counter](count_all_repo_stars.py) yourself and submit a pull request.
    ```bash
    python count_all_repo_stars.py --github-token $YOUR_GITHUB_TOKEN
    ```

    The line above would run over all public repositories. For a more manageable run, sample 1 million instead.
    ```bash
    python count_all_repo_stars.py --github-token $YOUR_GITHUB_TOKEN --sample-size 1000000
    ```

    Note I will not consider merging results with `--sample-size` below 1 million.