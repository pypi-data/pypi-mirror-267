import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='getcp',
    version='1.0.21',
    description='getcp is a Python package that provides functions to retrieve stats from Competitive Programming platforms. Currently, it supports fetching stats from CodeChef and Codeforces.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UD11/getcp-pkg",
    author='Uddalak Seal',
    author_email='hidan84@duck.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
    keywords='competitive programming codeforces codechef api scraper',
    project_urls={
        'Documentation': 'https://ud11.github.io/getcp-docs/',
        'Source': 'https://github.com/UD11/getcp-pkg?tab=readme-ov-file',
        'Tracker': 'https://github.com/UD11/getcp-pkg/issues',
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    python_requires='>=3.6',
)
