#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Show help for py_whycon_code
'''
import os, sys

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))

PACKAGE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin'))
sys.path.append(PACKAGE_DIR)

if __name__ == "__main__":

    import whycon
    help(whycon)