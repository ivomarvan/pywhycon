#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Help function for setup.py
'''
import subprocess
import os
from os.path import join, abspath, realpath, dirname
from os import walk
import re


THE_DIR=dirname(__file__)

# join and made abs
def abs_path(*args) -> str:
    return abspath(join(*args))


# find sources
def get_files(dirs: [str], relative_to_root: str = THE_DIR, extension: str = None, relative: bool = False) -> [str]:
    ret_list = []
    if isinstance(dirs, str):
        dirs = [dirs]
    for dir in dirs:
        root, _, filenames = next(walk(dir))
        filtered_filenames = []
        for file in filenames:
            if extension is None or file.endswith(extension):
                filtered_filenames.append(file)
        if relative:
            relative_dir = '.' + abspath(root)[len(abspath(relative_to_root)):]
            filtered_filenames = [join(relative_dir, file) for file in filtered_filenames]
        else:
            filtered_filenames = [abs_path(root, file) for file in filtered_filenames]
        ret_list += filtered_filenames
    return ret_list

def shell(command: [str] ) -> str:
    '''
    Call shell (ssh, bash, ...) and return result.
    '''
    return subprocess.check_output(command).decode(encoding='UTF-8').strip()

VERSION_RE = re.compile(r'^[v]?(([0-9]+)\.([0-9]+)\.([0-9]+))')

def get_version() -> str:
    # Try find it in the root directory from the git
    version_filename = os.path.join(THE_DIR, 'VERSION.txt')
    try:
        command = ['git', 'describe', '--tags']
        version_string = shell(command)
        # first becor '-'
        version_string = version_string.split('-')[0]
        match = VERSION_RE.match(version_string)
        if match:
            found_version = match[0]
            with open(version_filename, 'w') as f:
                f.write(found_version + '\n')
            return found_version
        else:
            raise Exception('No good tags found for verion in git.')
    except:
        # If no git is here, try read it from txt file
        with open(version_filename, 'r') as f:
            return f.read().strip()


if __name__ == "__main__":
    print(get_version())