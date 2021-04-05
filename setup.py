#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ivo Marvan'
__email__ = 'ivo@marvan.cz'
__description__ = '''
    Setup for whycon.
    
    ./setup.py install
    
    1) Build the whycon_core library (into ./whycon_core/bin/whycon_core.so)
         (In the BuildExtWhyconSo::run method by calling an external Makefile)
    2) Build a wrapper, by standard means setup.py
         (Extension (...), call super().run() in BuildExtWhyconSo::run
    3) Installs the whycon wrapper library into the actual python environment
'''

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


import os
import pkgconfig

# The directory containing this file
THE_DIR = os.path.dirname(__file__)

# helping functions
from utils import abs_path, get_files, shell

# --- Constants (directories ect.) -------------------------------------------------------------------------------------
USED_OPENCV = 'opencv4' # OR opencv
VERSION = '1.0.0'  # @todo Generate from git tag

WHYCON_CORE_DIR = abs_path(THE_DIR, 'whycon_core')
WHYCON_CORE_SRC_DIR = abs_path(WHYCON_CORE_DIR, 'src')
WHYCON_CORE_LIB_DIR = abs_path(WHYCON_CORE_DIR, 'bin')
PYWHYCON_SRC_DIR    = abs_path(THE_DIR, 'src')
PYWHYCON_BUILD_DIR  = abs_path(THE_DIR, 'build')
PY_MAKEFILE         = abs_path('.', 'Makefile')
WHYCON_CORE_MAKEFILE = abs_path('.', 'whycon_core', 'Makefile')


# compile params for module whycon.so
PY_CXXFLAGS = ''
PY_CXXFLAGS += '-Wall -fPIC -O3 -shared -std=gnu++11 ' # + shell(['python3-config', '--cflags']) + ' '
#PY_CXXFLAGS += '-I/usr/include' + ' '
# compile params, use same version of opencv as python
PY_CXXFLAGS += pkgconfig.cflags(USED_OPENCV)

whycon_python_wrapper = Extension(
    'whycon',
    sources=get_files(PYWHYCON_SRC_DIR, extension='.cpp'),
    extra_compile_args=PY_CXXFLAGS.split(' '),
    extra_link_args=[os.path.abspath('./whycon_core/bin/whycon_core.so')]
)


# The text of the README file
with open(os.path.join(THE_DIR, 'README.md'), 'r') as f:
    README = f.read()
with open(os.path.join(WHYCON_CORE_DIR, 'README.md'), 'r') as f:
    README += f.read()

class BuildExtWhyconSo(build_ext):
    def run(self):
        # compile library to whycon_core/bin/whycon.so
        makefile_dir = WHYCON_CORE_DIR
        command = ['make', '-C', makefile_dir, f'SYS_LIB_DIR={WHYCON_CORE_LIB_DIR}']
        print(' '.join(command))
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
        'numpy',
        'pybind11',
        # 'opencv-python' | cv2
    ],
    ext_modules = [whycon_python_wrapper],
    cmdclass={'build_ext': BuildExtWhyconSo},
)



