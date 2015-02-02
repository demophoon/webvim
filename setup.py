#!/usr/bin/env python
from setuptools import setup

setup(
    name="webterm",
    version="0.1.0",
    author="Britt Gresham",
    author_email="brittcgresham@gmail.com",
    description=("Stream terminal applications to the web browser"),
    license="AGPL v3.0",
    install_requires=[
        'tornado',
        'sockjs-tornado',
    ],
    entry_points="""
    [console_scripts]
    webterm_server=webvim.app:main
    """
)
