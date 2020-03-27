"""Generates a thermal image based on the number of times each pixel exceeds a temperature threshold"""
import argparse
import np_vid_viewer.composite as composite

PARSER = argparse.ArgumentParser(description='Analyze temperature data.')
PARSER.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
PARSER.add_argument('THRESHOLD',
                    type=int,
                    help='temperature theshold of the image')

ARGS = PARSER.parse_args()

TEMP_DATA_FILE = ARGS.temp_data
THRESHOLD = ARGS.THRESHOLD

composite.generate_threshold_image(TEMP_DATA_FILE, threshold=THRESHOLD)
