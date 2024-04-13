import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='getcp',
    version='1.0.0',
    description='get cp stats of users with the help of their usernames',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='uddalak seal',
    author_email='hidan84@duck.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
    ],
    license='MIT'
)
