import argparse
import np_vid_viewer

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
parser.add_argument('start', type=int, help='first frame of the video.')
parser.add_argument('end', type=int, help='last frame of the video.')
parser.add_argument(
    '-follow', type=int, default=False, required=False, help='0 or 1 specifying wether or not to follow the meltpool in the video'
)
parser.add_argument('-framerate',
                    type=int,
                    default=60,
                    required=False,
                    help='Framerate of the video')
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

parser.add_argument(
    '--build',
    type=str,
    default=None,
    required=False,
    help='Name of build'
)

args = parser.parse_args()

<<<<<<< HEAD:save_partial_video.py
DATA_DIRECTORY = args.data_directory
=======
build = args.build
temp_data_file = args.temp_data
merged_data_file = args.merged_data
>>>>>>> rjBranch:view.py
scale_factor = args.scale
top = bool(args.top)
bot = bool(args.bot)
show_max = bool(args.showmax)
FRAMERATE = args.framerate
FOLLOW = bool(args.follow)
start = args.start
end = args.end

<<<<<<< HEAD:save_partial_video.py
VIEWER = np_vid_viewer.NpVidTool(data_directory=DATA_DIRECTORY,
=======
VIEWER = np_vid_viewer.NpVidTool(build=build,
                                temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
>>>>>>> rjBranch:view.py
                                 scale_factor=scale_factor,
                                 mp_data_on_vid=args.mp,
                                 remove_top_reflection=top,
                                 remove_bottom_reflection=bot,
                                 circle_max_temp=show_max,
                                 follow_meltpool=FOLLOW)

VIEWER.save_partial_video(start=start, end=end, framerate=FRAMERATE)
