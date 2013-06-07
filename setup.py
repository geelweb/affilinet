#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages
import affilinet

setup(
    name = "Affilinet",
    version = affilinet.__version__,
    packages = find_packages(exclude=["examples", "tests"]),
    author = "Guillaume Luchet",
    author_email = "guillaume@geelweb.org",
    description = "Affilinet Client",
    license = "MIT License",
    keywords = "Affilinet Client affiliation",
    platforms = "ALL"
)
