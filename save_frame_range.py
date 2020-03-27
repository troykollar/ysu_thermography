import np_vid_viewer

import argparse

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
parser.add_argument('merged_data',
                    type=str,
                    help='the file location/name of the merged data')
parser.add_argument('start', type=int, help='first frame to save')
parser.add_argument('end', type=int, help='last frame to save')
parser.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')

args = parser.parse_args()

temp_data_file = args.temp_data
merged_data_file = args.merged_data
scale_factor = args.scale
start = args.start
end = args.end

VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
                                 scale_factor=scale_factor)

VIEWER.save_frame_range16(start, end)