from setuptools import setup, find_packages

setup(
    name="git-star-percentile",
    version="0.1",
    packages=find_packages(),
    install_requires=["pandas", "requests"],
    entry_points={
        "console_scripts": [
            "git-star-percentile=git_star_percentile.__main__:main",
        ],
    },
)
