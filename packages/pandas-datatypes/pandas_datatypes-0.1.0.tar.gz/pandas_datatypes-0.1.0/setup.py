from setuptools import setup, find_packages

setup(
    name="pandas_datatypes",
    version="0.1.0",
    author="Brajesh",
    description="A library for geting correct datatype from pandas dataFrame",
    packages=find_packages(include=["pandas_datatypes", "pandas_datatypes.*"]),
    install_requires=[
        "pandas",
    ],
)