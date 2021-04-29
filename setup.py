#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ivo Marvan'
__email__ = 'ivo@marvan.cz'
__description__ = '''
    Setup for whycon.
    
    ./setup.py install
    
    1) Build the whycon_core library (into ./whycon_core/build/*.o)
         (In the BuildExtWhyconSo::run method by calling an external Makefile)
    2) Build a wrapper whycon.so         
    3) Installs the whycon wrapper library into the actual python environment
'''
import os
import sys
try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
    from setuptools.command.build_clib import build_clib
    print('The setuptools is used.')
except ImportError as e:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext
    from distutils.command.build_clib import build_clib
    print('The distutils is used.')

# The directory containing this file
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)

# helping functions
from utils import get_version, abs_path, shell

WHYCON_CORE_DIR = abs_path(PROJECT_ROOT, 'whycon_core')



# --- Constants (directories ect.) -------------------------------------------------------------------------------------
USED_OPENCV = 'opencv4' # OR opencv
VERSION = get_version()

# The text of the README file
with open(os.path.join(PROJECT_ROOT, 'README.md'), 'r') as f:
    README = f.read()
with open(os.path.join(WHYCON_CORE_DIR, 'README.md'), 'r') as f:
    README += f.read()

# --- Buildin ----------------------------------------------------------------------------------------------------------
class BuildExtWhyconSo(build_ext):
    def run(self):
        # compile library whycon_core
        command = ['make']
        print(command)
        print(shell(command))
        super().run()




# This call to setup() does all the work
setup(
    name='whycon',
    version=VERSION,
    description='Python wrapper for Whycon (Whycode),  precise, efficient and low-cost localization system',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ivomarvan/pywhycon',
    author='Ivo Marvan',
    author_email='ivo@marvan.cz',
    keywords=['localization', 'whycode', 'whycon'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
    install_requires=[
        'numpy',        # for sharing images between Python and C++
        'pybind11',     # create python package from C++
        'pkgconfig',     # found good version of OpenCv in a environment
        'opencv-python'           # 'opencv-python' in pip but can be different in conda
    ],
    cmdclass={'build_ext': BuildExtWhyconSo},
)



