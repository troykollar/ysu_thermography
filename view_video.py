import argparse
import cv2
import numpy as np
import datetime
import os
import np_vid_viewer

PARSER = argparse.ArgumentParser()
PARSER.add_argument("directory", type=str, help="Directory containing files.")

ARGS = PARSER.parse_args()

DIR = ARGS.directory

os.chdir(DIR)

VIEWER = np_vid_viewer.NpVidViewer(
    "thermal_cam_temps.npy",
    melt_pool_data="melt_pool_data.npy",
    tc_times="thermal_cam_times.npy",
    remove_reflection=True,
    remove_lower=True,
)

VIEWER.generate_video()
