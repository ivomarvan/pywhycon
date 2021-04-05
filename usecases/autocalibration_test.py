#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Read images from camera and use whycon module.
    
    Calibration of coordinate transformation using 4 marks arranged in a square.
    Calibration is completed by finding a sufficient number of images with 4 marks found.
    
'''
import os
import sys
from time import time, sleep

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
#PACKAGE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin'))
sys.path.append(THE_FILE_DIR)
#sys.path.append(PACKAGE_DIR)

from whycon import WhyCodeDetector, SpaceTransofmType as TransType
from web_camera import WebCamera
from window import ImgStorageWindow


if __name__ == "__main__":
    # import py_whycon_code; help(py_whycon_code); exit()
    debug = True

    camera_calibration_path = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'camera_calibration.example.yml'))
    space_calibration_path_in  = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'space_calibration.example.yml'))
    space_calibration_path_out = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'space_calibration.autocalibration_result.yml'))

    # print('camera_calibration_path', camera_calibration_path)
    # print('space_calibration_path_in', space_calibration_path_in)

    window = ImgStorageWindow()

    camera = WebCamera()

    
    detector = WhyCodeDetector(
        camera_calibration_path,    # path to existing camera calibration file
        space_calibration_path_in,  # path to existing space calibration file
        0.15,   # default black circle diameter [m];
        4,      # num of markers to track
        TransType.T_NONE,  # calibation transform type
        7,     # num of ID id_bits
        720,    # num of id_samples to identify ID
        2,      # hamming distance of ID code
        True,   # whether to identify ID
        True,   # whether to show coords
        True,   # whether to show segment
        False   # whether print debug info
    )

    stop = False
    t_sum = 0.0
    t_count = 0

    while not stop:
        detector_result = None
        img_array, timestamp_ms = camera.read()
        if img_array is not None:
            start_time = time()

            autocalib_results = detector.detect_and_calibrate(
                img_array, space_calibration_path_out, 1.0, 1.0, debug
            )
            stop_time = time()
            if autocalib_results:
                for i, marker in enumerate(autocalib_results.markers):
                    print(f'\t\tID {marker.segment_in_image.ID}')
                    print(f'{i}\t\tin image x:{marker.segment_in_image.x}, y:{marker.segment_in_image.y}')
                    print(f'\t\tin space x:{marker.coords.x}, y:{marker.coords.y}, z:{marker.coords.z}, d:{marker.coords.d}')
                stop = autocalib_results.saved
            window.swow(img_array)
            delta_time = stop_time - start_time
            t_sum += delta_time
            t_count += 1
        # print(f'delta time = {delta_time}')
        if not stop:
            stop = window.is_stopped()
    print(f'AVG(delta time) = {round(1000*delta_time, 1)} [ms]')


