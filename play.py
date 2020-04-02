"""Uses NpVidTool to generate and play a video with cv2.imshow()"""
import argparse
import np_vid_viewer


def get_extension(filename: str):
    """Returns the file extensino of a given filename."""
    return filename[filename.rfind('.'):]


def validate_extension(argument_name: str, filename: str,
                       required_extension: str):
    """Returns true if the extension of a given filename does not equal the required_extension"""
    error = False
    if get_extension(filename) != required_extension:
        print(argument_name + " must be of type '" + required_extension + "'")
        error = True
    return error


PARSER = argparse.ArgumentParser(description='Analyze temperature data.')
PARSER.add_argument('data_directory',
                    type=str,
                    help='the file location/name of the temperature data')
PARSER.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')
PARSER.add_argument(
    '-delay',
    type=int,
    default=1,
    required=False,
    help=
    'int specifying millisecond delay between showing each frame in play_video()'
)
PARSER.add_argument(
    '-mp',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to overlay meltpool data on the image'
)
PARSER.add_argument(
    '-top',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to remove top reflections')
PARSER.add_argument(
    '-bot',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to remove bottom reflections')
PARSER.add_argument(
    '-showmax',
    type=int,
    default=False,
    required=False,
    help=
    '0 or 1 specifying whether or not to highlight the max temp of the frame')

ARGS = PARSER.parse_args()

ARGUMENT_ERROR = False
# Validate temp_data file input
DATA_DIRECTORY = ARGS.data_directory

#TODO: Validate directory
DATA_DIRECTORY_ERROR = False

ARGUMENT_ERROR = DATA_DIRECTORY_ERROR

SCALE_FACTOR = ARGS.scale
FRAME_DELAY = ARGS.delay
REMOVE_TOP_REFLECTION = bool(ARGS.top)
REMOVE_BOTTOM_REFLECTION = bool(ARGS.bot)
SHOW_MAX = bool(ARGS.showmax)

if ARGUMENT_ERROR:
    pass
else:
    VIEWER = np_vid_viewer.NpVidTool(
        data_directory=DATA_DIRECTORY,
        scale_factor=SCALE_FACTOR,
        mp_data_on_vid=ARGS.mp,
        remove_top_reflection=REMOVE_TOP_REFLECTION,
        remove_bottom_reflection=REMOVE_BOTTOM_REFLECTION,
        circle_max_temp=SHOW_MAX)

    VIEWER.play_video(FRAME_DELAY)
