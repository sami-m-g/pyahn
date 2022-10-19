#!/usr/bin/env python

from setuptools import setup, find_packages

from pyahn import __version__


def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="pyahn",
    version=__version__,
    description="A python package for extracting the Z values for a set of XY coordinates from AHN4",
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
        "numpy==1.23.3",
        "tifffile==2022.4.8"
    ],
    tests_require=[
        "pytest==7.1.3",
        "pytest-cov==4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "pyahn-main=pyahn.tile:main"
        ]
    },
    package_data={
        "pyahn": [
            "data/*.*"
        ]
    }
)