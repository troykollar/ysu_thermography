import argparse
import np_vid_viewer

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
parser.add_argument('merged_data',
                    type=str,
                    help='the file location/name of the merged data')
parser.add_argument('save_dst',
                    type=str,
                    help='destination folder to save frame png')
parser.add_argument('frame_num',
                    type=int,
                    help='index of the frame to be saved')

args = parser.parse_args()

temp_data_file = args.temp_data
merged_data_file = args.merged_data
save_dst = args.save_dst
frame_num = args.frame_num

VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file)

VIEWER.save_frame16(frame_num, save_dst)
