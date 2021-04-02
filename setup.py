#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Setup for pywhycon.
'''

import pathlib
from setuptools import setup
#from setuptools.command.

import subprocess
import sys

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pywhycon",
    version="1.0.0",
    description="Python wrapper for Whycon (Whycode),  precise, efficient and low-cost localization system",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ivomarvan/pywhycon",
    author="Ivo Marvan",
    author_email="ivo@marvan.cz",
    keywords=['localization', 'whycode', 'whycon'],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["pywhycon"],
    include_package_data=True,
    install_requires=["cv2", "numpy"],
    entry_points={ "console_scripts": [] },
)

'''
class Build(build):
    """Customized setuptools build command - builds protos on build."""
    def run(self):
        protoc_command = ["make"]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)
        build.run(self)
'''