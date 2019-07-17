#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="lwday",
    version='0.1',
    author="Erin Kado-Fong",
    author_email="kadofong@princeton.edu",
    packages=["lwday"],
    url="https://github.com/ekadofong/lwday",
    license="MIT",
    description="barebones day planner",
)
