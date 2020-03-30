import argparse
import np_vid_viewer

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
parser.add_argument('merged_data',
                    type=str,
                    help='the file location/name of the merged data')
parser.add_argument('start', type=int, help='first frame of the video.')
parser.add_argument('end', type=int, help='last frame of the video.')
parser.add_argument('-speed',
                    type=int,
                    default=15,
                    required=False,
                    help='Speed of video playback as it relates to real time')
parser.add_argument('-real_fps',
                    type=int,
                    default=4,
                    required=False,
                    help='realtime framerate thermal video was captured in')
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

temp_data_file = args.temp_data
merged_data_file = args.merged_data
scale_factor = args.scale
top = bool(args.top)
bot = bool(args.bot)
show_max = bool(args.showmax)
speed = args.speed
real_fps = args.real_fps
start = args.start
end = args.end

VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
                                 scale_factor=scale_factor,
                                 mp_data_on_vid=args.mp,
                                 remove_top_reflection=top,
                                 remove_bottom_reflection=bot,
                                 circle_max_temp=show_max)

VIEWER.save_partial_video(start=start,
                          end=end,
                          playback_speed=speed,
                          realtime_framerate=real_fps)
