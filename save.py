import argparse
import np_vid_viewer

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
parser.add_argument('-framerate',
                    type=int,
                    default=60,
                    required=False,
                    help='Framerate of the video to be saved.')
parser.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')
parser.add_argument(
    '-mp',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to overlay meltpool data on the image'
)
parser.add_argument(
    '-top',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to remove top reflections')
parser.add_argument(
    '-bot',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to remove bottom reflections')
parser.add_argument(
    '-showmax',
    type=int,
    default=False,
    required=False,
    help=
    '0 or 1 specifying whether or not to highlight the max temp of the frame')

args = parser.parse_args()

DATA_DIRECTORY = args.data_directory
scale_factor = args.scale
top = bool(args.top)
bot = bool(args.bot)
show_max = bool(args.showmax)
FRAMERATE = args.framerate

VIEWER = np_vid_viewer.NpVidTool(data_directory=DATA_DIRECTORY,
                                 scale_factor=scale_factor,
                                 mp_data_on_vid=args.mp,
                                 remove_top_reflection=top,
                                 remove_bottom_reflection=bot,
                                 circle_max_temp=show_max)

VIEWER.save_video(framerate=FRAMERATE)
