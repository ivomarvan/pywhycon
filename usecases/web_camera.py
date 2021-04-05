#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Camera image source.
    
    Searches for a connected camera (that is not shaded).
'''
import sys
import os
import cv2
import numpy as np

class WebCamera:
    """
    Camera input.
    An active switched-on camera whose number is in the given range is searched for.
    """
    def __init__(self, range_of_camera_ids: range = range(10)):
        self._capture = None
        self._is_adjusted = False
        self._range_of_camera_ids = range_of_camera_ids

    def __del__(self):
        if not self._capture is None:
            self._capture.release()

    def _get_img(self) -> (np.ndarray, int):
        ret, img = self._capture.read()
        # Int id of image. In the case of camera it can be "Current position of the video file in microseconds".
        img_microseconds = int(1000 * self._capture.get(cv2.CAP_PROP_POS_MSEC))
        return img, img_microseconds

    def _img_is_ok(self, img_array: np.ndarray, deep_check: bool=False, treshold: int = 100):
        if img_array is None:
            return False
        if deep_check:
            # test for some 'sweet' colors
            if np.sum(img_array > 100) < treshold:
                return False
        return True

    def _adjust_and_return_img(self) -> (np.ndarray, int):
        for i in self._range_of_camera_ids:
            try:
                self._capture = cv2.VideoCapture(i)
            except Exception as e:
                print(e)
            if self._capture.isOpened():
                img, img_microseconds = self._get_img()
                if self._img_is_ok(img, deep_check=True):
                    print('-' * 80)
                    print('Found camera:', i)
                    print('-' * 80)
                    return img, img_microseconds
        return None, None

    def read(self) -> (np.ndarray, int):
        if not self._is_adjusted:
            # first initialization
            img_array, img_microseconds = self._adjust_and_return_img()
        else:
            img_array, img_microseconds = self._get_img()

        self._is_adjusted = self._img_is_ok(img_array)

        if self._is_adjusted:
            timestamp_ms=1000 * img_microseconds
            return img_array, timestamp_ms
        else:
            return img_array, -1
