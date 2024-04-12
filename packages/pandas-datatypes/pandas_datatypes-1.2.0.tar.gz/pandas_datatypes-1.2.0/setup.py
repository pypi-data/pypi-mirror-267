from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pandas_datatypes",
    version="1.2.0",
    author="Brajesh",
    description="A library for getting correct datatype from pandas DataFrame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["pandas_datatypes", "pandas_datatypes.*"]),
    install_requires=[
        "pandas",
    ],
)