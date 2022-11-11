#!/usr/bin/env python

from setuptools import setup, find_packages

from pyahn import __version__


def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="pyahn",
    version=__version__,
    description="A python package for extracting the Z values for a set of XY coordinates from AHN",
    long_description=readme(),
    author="Mina Sami",
    author_email="sami.mg@outlook.com",
    url="https://github.com/sami-m-g",
    packages=find_packages(
        include=[
            "pyahn"
        ]
    ),
    install_requires=[
        "ellipsis==3.0.2",
        "geopandas==0.9.0",
        "matplotlib==3.6.2",
        "pandas==1.5.0"
    ],
    tests_require=[
        "coverage==6.5.0",
        "pytest==7.1.3"
    ],
    entry_points={
        "console_scripts": [
            "pyahn-main=pyahn.core:main"
        ]
    },
    package_data={
        "pyahn": [
            "data/*.*"
        ]
    }
)