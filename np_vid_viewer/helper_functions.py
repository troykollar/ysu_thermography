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
