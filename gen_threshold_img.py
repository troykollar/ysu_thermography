import argparse
import np_vid_viewer
import np_vid_viewer.composite as composite

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
parser.add_argument('threshold',
                    type=int,
                    help='temperature theshold of the image')

args = parser.parse_args()

temp_data_file = args.temp_data
threshold = args.threshold

composite.generate_threshold_image(temp_data_file, threshold=threshold)
