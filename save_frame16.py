import argparse
import np_vid_viewer

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
parser.add_argument('save_dst',
                    type=str,
                    help='destination folder to save frame png')
parser.add_argument('frame_num',
                    type=int,
                    help='index of the frame to be saved')

args = parser.parse_args()

DATA_DIRECTORY = args.data_directory
save_dst = args.save_dst
frame_num = args.frame_num

VIEWER = np_vid_viewer.NpVidTool(data_directory=DATA_DIRECTORY)

VIEWER.save_frame16(frame_num, save_dst)
