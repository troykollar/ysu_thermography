import np_vid_viewer

import argparse

PARSER = argparse.ArgumentParser(description='Analyze temperature data.')
PARSER.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
PARSER.add_argument('-framerate',
                    type=int,
                    default=60,
                    required=False,
                    help='Framerate of the video')
PARSER.add_argument(
    '-img',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to save image after video')
PARSER.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')

args = PARSER.parse_args()

DATA_DIRECTORY = args.data_directory
FRAMERATE = args.framerate
IMG = args.img
scale_factor = args.scale

VIEWER = np_vid_viewer.NpVidTool(data_directory=DATA_DIRECTORY,
                                 scale_factor=scale_factor)

VIEWER.save_hotspot_video(framerate=FRAMERATE, save_img=IMG)