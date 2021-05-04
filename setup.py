#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ivo Marvan'
__email__ = 'ivo@marvan.cz'
__description__ = '''
    Setup for whycon.
    
    ./setup.py install
    
    Build the whycon_core library (into ./whycon_core/build/*.o) and wrapper whycon.so       
    (In the BuildExtWhyconSo::build_extension method by calling an external Makefile)
      
    Installs the whycon wrapper library into the actual python environment.
'''
import os
import sys
from multiprocessing import cpu_count
from subprocess import call

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

whycon_extension = Extension(
    'whycon', 
    sources = [],  # Makefile and Manifest.in cares about it
    libraries = ['whycon.so'],
    library_dirs = ['bin/']
)

# --- Buildin ----------------------------------------------------------------------------------------------------------
class BuildExtWhyconSo(build_ext):
    def build_extension(self, ext):
        '''
        @inspiration https://stackoverflow.com/questions/41169711/python-setuptools-distutils-custom-build-for-the-extra-package-with-makefile
        '''
        if ext.name != whycon_extension.name:
            # Handle regular extension
            return super().build_extension(ext)

        # Handle special extension
        cmd = ['make']
        try:
            j = max(cpu_count() - 1, 1)
            cmd.append('-j')
            cmd.append(str(j))
        except NotImplementedError:
            print('Unable to determine number of CPUs. Using single threaded make.')

        print('BuildExtWhyconSo:', ' '.join(cmd))
        err_code = call(cmd)

        if err_code != 0:
            # @todo react in case or error in make process
            pass

        # copy resulting tool to library build folder
        make_result_file = os.path.join(PROJECT_ROOT, 'bin', 'whycon.so')
        setup_result_file = self.get_ext_fullpath(ext.name)
        self.mkpath(self.build_lib)
        os.makedirs(self.build_lib, exist_ok=True)
        self.copy_file(make_result_file, setup_result_file)


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
        'opencv-python>=4.5.1' # 'opencv-python' in pip but can be different in conda
    ],
    ext_modules = [whycon_extension],
    cmdclass={'build_ext': BuildExtWhyconSo},
)



