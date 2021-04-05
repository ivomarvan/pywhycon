#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Show image in window, wait for closing or char "q" or "<ESC>.
'''
import cv2
import numpy as np

class ImgStorageWindow:

    def __init__(self, name: str = 'Python_images', type: int = cv2.WINDOW_NORMAL):
        self._name = name
        cv2.namedWindow(self._name, type)

    def swow(self, img_array: np.ndarray) -> bool:
        if img_array is None:
            return True
        cv2.imshow(self._name, img_array)
        return True

    def is_stopped(self) -> bool:
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            return True
        return cv2.getWindowProperty(self._name, cv2.WND_PROP_VISIBLE) < 1