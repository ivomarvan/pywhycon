#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Read images from a camera and use whycon module to find markers.
'''
import os
import sys
from time import time, sleep

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

try:
    from whycon import WhyCodeDetector, SpaceTransofmType as TransType
    import whycon
    print(f'Use installed whycon package in "{whycon.__file__}"')
except ModuleNotFoundError:
    PACKAGE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin'))
    sys.path.append(PACKAGE_DIR)
    from whycon import WhyCodeDetector, SpaceTransofmType as TransType
    print(f'Use whycon paskage from local installation: "{PACKAGE_DIR}"')

from web_camera import WebCamera
from window import ImgStorageWindow


if __name__ == "__main__":
    # import py_whycon_code; help(py_whycon_code); exit()
    debug = True

    camera_calibration_path = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'camera_calibration.example.yml'))
    space_calibration_path  = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'space_calibration.example.yml'))

    # print('camera_calibration_path', camera_calibration_path)
    # print('space_calibration_path', space_calibration_path)

    window = ImgStorageWindow()

    camera = WebCamera()

    detector = WhyCodeDetector(
        camera_calibration_path, # path to existing camera calibration file
        space_calibration_path,  # path to existing space calibration file
        0.15,             # default black circle diameter [m];
        4,                # num of markers to track
        TransType.T_NONE, # calibation transform type
        7,                # num of ID id_bits
        720,              # num of id_samples to identify ID
        2,                # hamming distance of ID code
        True,             # whether to identify ID
        True,             # whether to show coords
        True,             # whether to show segment
        False             # whether print debug info
    )

    stop = False
    t_sum = 0.0
    t_count = 0

    while not stop:
        detector_result = None
        img_array, timestamp_ms = camera.read()
        if img_array is not None:
            start_time = time()
            detector_result = detector.detect(img_array)
            stop_time = time()
            if detector_result:
                for i, marker in enumerate(detector_result):
                    print(f'\t\tID {marker.segment_in_image.ID}')
                    print(f'{i}\t\tin image x:{marker.segment_in_image.x}, y:{marker.segment_in_image.y}')
                    print(f'\t\tin space x:{marker.coords.x}, y:{marker.coords.y}, z:{marker.coords.z}, d:{marker.coords.d}')
            window.swow(img_array)
            delta_time = stop_time - start_time
            t_sum += delta_time
            t_count += 1
        # print(f'delta time = {delta_time}')
        stop = window.is_stopped()
    print(f'AVG(delta time) = {round(1000*delta_time, 1)} [ms]')


