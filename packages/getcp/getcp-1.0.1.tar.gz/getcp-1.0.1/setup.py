import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='getcp',
    version='1.0.1',
    description='getcp is a Python package that provides functions to retrieve stats from CP platforms. Currently, it supports fetching stats from CodeChef and Codeforces.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Uddalak Seal',
    author_email='hidan84@duck.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    license='MIT'
)