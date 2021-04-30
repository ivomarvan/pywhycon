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
import subprocess

# Sigleton
class OpenCV_params:

    OPENCV_MASK_RE = re.compile(r'(opencv[^\.]*)\.pc')  # opencv4.pc  or opencv.pc
    HOME_DIR = os.path.expanduser('~')

    def __init__(self):
        found_paskages = self._find_in_tree(root=os.path.dirname(cv2.__file__))
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

    def _find_in_dir_python(self, root_dir: str, exclude_dirs: []) -> [(str, str)]:
        mask_re = self.OPENCV_MASK_RE
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

    def _find_in_dir_shell(self, root_dir: str, exclude_dir: str = '') -> [(str, str)]:
        mask_re = self.OPENCV_MASK_RE
        mask: str = 'opencv*.pc'
        command = fr'find {root_dir} -name "{mask}"'
        if exclude_dir:
            command += f' -not -path "./{exclude_dir}/*"'
        # print(command)
        out = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Get standard out and error
        (stdout, stderr) = out.communicate()

        # Save found files to list
        found_list = stdout.decode().split()
        if found_list == []:
            return []
        return [(mask_re.search(os.path.basename(f))[1], os.path.dirname(f))for f in found_list]

    def _find_in_dir(self, root_dir: str, exclude_dirs: []) -> [(str, str)]:
        '''
        Try it quickly by shell. If it failed, try it by python.
        '''
        try:
            if len(exclude_dirs) > 0:
                exclude_dir = exclude_dirs[0]
            else:
                exclude_dir = ''
            return self._find_in_dir_shell(root_dir=root_dir, exclude_dir=exclude_dir)
        except Exception:
            return self._find_in_dir_python(root_dir=root_dir, exclude_dirs=exclude_dirs)


    def _find_in_tree(self, root:str = os.path.dirname(cv2.__file__)) -> [(str, str)]:
        exclude_dirs = []
        while True:
            if root == os.path.sep or root == self.HOME_DIR:
                return []
            # print('root', root, 'exclude_dirs', exclude_dirs)
            found_files = self._find_in_dir(root_dir=root, exclude_dirs=exclude_dirs)
            if found_files:
                return found_files
            root_parts = os.path.split(root)
            root = root_parts[0]
            exclude_dirs = [root_parts[1]]

    def get_as_env_variables(self) -> str:
        return f'CCLAGS += {self.cflags()}\n\tLIBS += {self.libs()} \n'

    def get_as_list(self) -> str:
        return f'"{self.cflags()}\n\tLIBS" "{self.libs()}"'

if __name__ == "__main__":
    p = OpenCV_params()
    print(p.get_as_list())
    # print('version:\t', p.version())
    # print('pkg_config_name:\t', p.pkg_config_name())
    # print('cflags:\t', p.cflags())
    # print('libs:\t', p.libs())
    # print('pkg_config_path:\t', p.pkg_config_path())
