import np_vid_viewer

import argparse

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
parser.add_argument('merged_data',
                    type=str,
                    help='the file location/name of the merged data')

args = parser.parse_args()

temp_data_file = args.temp_data
merged_data_file = args.merged_data

VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
                                 scale_factor=4,
                                 frame_delay=1,
                                 mp_data_on_vid=True,
                                 remove_top_reflection=True,
                                 remove_bottom_reflection=False)

VIEWER.play_video()
