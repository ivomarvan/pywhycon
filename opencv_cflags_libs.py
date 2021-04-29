#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
Finds parameters for compiling and linking a code with the OpenCV library.

The problem is that there can be multiple OpenCV installations on one computer.
It can be natural (by for example `apt install`), virtualenv,  conda virtual installation, etc.
Then it is necessary to find the parameters for the one that is current.
The pkg-config (pkgconfig in python) package is used for this.
However, the problem is setting the right PKG_CONFIG_PATH path.
'''

import os
import cv2
import re
import pkgconfig


# Sigleton
class OpenCV_params:

    OPENCV_MASK_RE = re.compile(r'(opencv[^\.]*)\.pc')  # opencv4.pc  or opencv.pc
    HOME_DIR = os.path.expanduser('~')

    def __init__(self):
        found_paskages = self._find_in_tree(root=os.path.dirname(cv2.__file__), mask_re=self.OPENCV_MASK_RE)
        if found_paskages:
            PKG_CONFIG_PATH = found_paskages[0][1]
            self._pkg_config_name = found_paskages[0][0]
            os.environ['PKG_CONFIG_PATH'] = PKG_CONFIG_PATH
            self._pkg_config_path = PKG_CONFIG_PATH
            self._cflags = pkgconfig.cflags(self._pkg_config_name)
            self._libs = pkgconfig.libs(self._pkg_config_name)
    
    def cflags(self) -> str:
        return self._cflags
    
    def libs(self) -> str:
        return self._libs
    
    def pkg_config_name(self) -> str:
        return self._pkg_config_name

    def version(self) -> str:
        return cv2.__version__

    def pkg_config_path(self) -> str:
        return self._pkg_config_path

    def _find_in_dir(self, root_dir: str, exclude_dirs: [], mask_re: re = OPENCV_MASK_RE) -> [(str, str)]:
        for root, dirs, files in os.walk(root_dir):
            # print('>', root, dirs, files)
            found_files = [(mask_re.search(f)[1], root) for f in files if mask_re.search(f) is not None]
            if found_files:
                return found_files
            for dir in dirs:
                if dir in exclude_dirs:
                    continue
                found_files = self._find_in_dir(os.path.join(root, dir), [])
                if found_files:
                    return found_files
        return []

    def _find_in_tree(self, root:str = os.path.dirname(cv2.__file__), mask_re: re = OPENCV_MASK_RE) -> [(str, str)]:
        exclude_dirs = []
        while True:
            if root == os.path.sep or root == self.HOME_DIR:
                return []
            print('root', root, 'exclude_dirs', exclude_dirs)
            found_files = self._find_in_dir(root_dir=root, exclude_dirs=exclude_dirs, mask_re=mask_re)
            if found_files:
                return found_files
            root_parts = os.path.split(root)
            root = root_parts[0]
            exclude_dirs = root_parts[1]


if __name__ == "__main__":
    p = OpenCV_params()
    print('version', p.version())
    print('pkg_config_name', p.pkg_config_name())
    print('cflags', p.cflags())
    print('libs', p.libs())
    print('pkg_config_path', p.pkg_config_path())

