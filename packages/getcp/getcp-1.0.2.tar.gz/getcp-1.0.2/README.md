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
    from getcp import cc, cf
    
    codechef_stats = cc.get_codechef_stats('username')
    codeforces_stats = cf.get_codeforces_stats('username')
    
    print("CodeChef Stats:")
    print(codechef_stats)
    
    print("\nCodeforces Stats:")
    print(codeforces_stats)


```