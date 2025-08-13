import numpy as np
import matplotlib.pyplot as plt
from git_star_percentile.__main__ import load_csv


def plot_star_distribution():
    df = load_csv()
    stars = df['stargazers_count'].dropna().astype(int)

    cutoffs = {
        'Top 1%': np.percentile(stars, 99),
        'Top 0.5%': np.percentile(stars, 99.5),
        'Top 0.2%': np.percentile(stars, 99.8),
        'Top 0.1%': np.percentile(stars, 99.9),
        'Top 0.05%': np.percentile(stars, 99.95),
        'Top 0.02%': np.percentile(stars, 99.98),
        'Top 0.01%': np.percentile(stars, 99.99),
    }

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['xtick.labelsize'] = 15
    plt.rcParams['ytick.labelsize'] = 15

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    stars = df['stargazers_count'].dropna().astype(int)
    stars_plus1 = stars + 1

    bins = np.logspace(np.log10(stars_plus1.min()), np.log10(stars_plus1.max()), 128)
    ax.hist(stars_plus1, bins=bins, color='white', edgecolor='#0F4D92', linewidth=1.5, alpha=0.8)
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Vertical percentile lines
    for label, value in cutoffs.items():
        ax.axvline(value, color='darkred', linestyle='--', linewidth=2)
        ax.text(
            value,
            ax.get_ylim()[1] * 0.1,
            f'{int(value)} stars' + r'$\rightarrow$' + f'{label}',
            rotation=90,
            va='center',
            ha='right',
            fontsize=10,
            color='black'
        )

    ax.set_xlabel('Number of Stars', fontsize=20)
    ax.set_ylabel('Number of repositories', fontsize=20)

    fig.tight_layout(pad=2)

    plt.savefig('./assets/github_stars_distribution.png', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    plot_star_distribution()
