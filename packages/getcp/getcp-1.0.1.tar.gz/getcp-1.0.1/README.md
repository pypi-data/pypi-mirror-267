# getcp

`getcp` is a Python package 
that provides functions to 
retrieve stats from CP
platforms. Currently, it supports user stats
from CodeChef and Codeforces.

## Installation

You can install `getcp` using pip:

```bash
pip install getcp
```

## Usage

```bash
    from getcp import get_codechef_stats, get_codeforces_stats

    codechef_stats = get_codechef_stats('my_codechef_username')
    codeforces_stats = get_codeforces_stats('my_codeforces_handle')
    
    print("CodeChef Stats:")
    print(codechef_stats)
    
    print("\nCodeforces Stats:")
    print(codeforces_stats)


```