"""Generates a thermal image based on the number of times each pixel exceeds a temperature threshold"""
import argparse
from np_vid_viewer.composite import generate_threshold_image

PARSER = argparse.ArgumentParser(description='Analyze temperature data.')
PARSER.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
PARSER.add_argument('THRESHOLD',
                    type=int,
                    help='temperature theshold of the image')
PARSER.add_argument('-start',
                    type=int,
                    default=0,
                    required=False,
                    help='First frame to consider.')
PARSER.add_argument('-end',
                    type=int,
                    default=0,
                    required=False,
                    help='Last frame to consider.')

ARGS = PARSER.parse_args()

TEMP_DATA_FILE = ARGS.temp_data
THRESHOLD = ARGS.THRESHOLD
START = ARGS.start
END = ARGS.end

generate_threshold_image(TEMP_DATA_FILE,
                         threshold=THRESHOLD,
                         start=START,
                         end=END)
