"""
Module for setting up the project.
"""

from setuptools import find_packages, setup

setup(
    name="chamco_ragbot",
    version="0.1.2",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    description="Hailstone calculator",
    author="Ibrahim Animashaun",
)


