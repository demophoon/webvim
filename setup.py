#!/usr/bin/env python
from setuptools import setup

setup(
    name = "webterm",
    version = "0.1.0",
    author = "Britt Gresham",
    author_email = "brittcgresham@gmail.com",
    description = ("Stream terminal applications to the web browser"),
    license = "MIT",
    install_requires=[
        'tornado',
        'sockjs-tornado',
    ],
)
