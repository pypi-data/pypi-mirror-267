# getcp

## Description

`getcp` is a Python package 
that provides functions to 
retrieve stats from CP
platforms. Currently, it supports user stats
from CodeChef and Codeforces.

### links

- [getcp-docs](https://ud11.github.io/getcp-docs/#currently-supported-platforms)
- [package link](https://pypi.org/project/getcp/)

## Installation

You can install `getcp` using pip:

```bash
pip install getcp
```

## Usage

```py
    from getcp import cc, cf, github
    
    codechef_stats = cc.get_codechef_stats('username')
    codeforces_stats = cf.get_codeforces_stats('username')
    github_info = github.get_github_stats('username')
    
    print("CodeChef Stats:")
    print(codechef_stats)
    
    print("\nCodeforces Stats:")
    print(codeforces_stats)
    
    print("\nGithub Info:")
    print(github_info)

```