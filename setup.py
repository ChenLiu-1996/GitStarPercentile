from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="git-star-percentile",
    version="1.1",
    license='MIT',
    author='Chen Liu',
    author_email='chen.liu.cl2482@yale.edu',
    packages=find_packages(),
    description='A simple tool to quantify your GitHub repo star percentile.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ChenLiu-1996/GitStarPercentile',
    keywords='GitHub, repository, star, popularity, percentile',
    install_requires=["pandas", "requests"],
    entry_points={
        "console_scripts": [
            "git-star-percentile=git_star_percentile.__main__:main",
        ],
    },
    classifiers=[
    'Development Status :: 3 - Alpha',         # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',         # Define that your audience are developers
    'License :: OSI Approved :: MIT License',  # Again, pick a license
    'Programming Language :: Python :: 3',     # Specify which pyhton versions that you want to support
    ],
)
