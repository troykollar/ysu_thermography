import np_vid_viewer

import argparse

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
parser.add_argument('start', type=int, help='first frame to save')
parser.add_argument('end', type=int, help='last frame to save')
parser.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')

args = parser.parse_args()

DATA_DIRECTORY = args.data_directory
scale_factor = args.scale
start = args.start
end = args.end

VIEWER = np_vid_viewer.NpVidTool(data_directory=DATA_DIRECTORY,
                                 scale_factor=scale_factor)

VIEWER.save_frame_range16(start, end)