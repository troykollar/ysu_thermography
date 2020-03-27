import np_vid_viewer
import numpy as np


def min_scale_factor(data_frame):
    """Given a frame of data, returns the minimum scale factor for the image to be at least 240x320"""
    height = data_frame.shape[0]
    width = data_frame.shape[1]

    scale_factor = 1
    while height * scale_factor < 240 or width * scale_factor < 320:
        scale_factor += 1

    return scale_factor


def get_build_folder(temp_filename: str):
    build_folder = temp_filename[:temp_filename.rfind('/')]
    return build_folder


def get_build_number(temp_filename: str):
    build_folder = get_build_folder(temp_filename)
    build_number = build_folder[:build_folder.find('_')]
    build_number = build_number[(build_number.rfind('/') + 1):]
    return build_number
