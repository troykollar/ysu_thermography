import argparse
import cv2
import numpy as np
import datetime
import os
from np_vid_viewer import NpVidViewer

PARSER = argparse.ArgumentParser()
PARSER.add_argument("directory", type=str, help="Directory containing files.")

ARGS = PARSER.parse_args()

DIR = ARGS.directory

os.chdir(DIR)

VIEWER = NpVidViewer(
    "thermal_cam_temps.npy",
    melt_pool_data="melt_pool_data.npy",
    tc_times="thermal_cam_times.npy",
    remove_reflection=True,
    remove_lower=True,
)

VIEWER.play_video(1)
