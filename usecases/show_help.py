#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Show help for whycon package.
'''
import os, sys

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

try:
    import whycon
    print(f'Use installed whycon package in "{whycon.__file__}"')
except ModuleNotFoundError:
    PACKAGE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin'))
    sys.path.append(PACKAGE_DIR)
    import whycon
    print(f'Use whycon paskage from local installation:"{PACKAGE_DIR}"')

if __name__ == "__main__":
    help(whycon)