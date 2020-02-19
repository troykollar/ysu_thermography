import argparse
import cv2
import numpy as np
import datetime
import os
import video_tools

PARSER = argparse.ArgumentParser()
PARSER.add_argument("directory", type=str, help="Directory containing files.")

ARGS = PARSER.parse_args()

DIR = ARGS.directory

os.chdir(DIR)

VideoTool = video_tools.NpVidTool(remove_reflection=True,
                                  remove_lower=True,
                                  mp_data_on_img=True)

VideoTool.generate_video(True)
