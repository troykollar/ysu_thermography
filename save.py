import argparse
import np_vid_viewer
import np_vid_viewer.dataset as dset

parser = argparse.ArgumentParser(description='Analyze temperature data.')
parser.add_argument('data_directory',
                    type=str,
                    help='the location of the data')
PARSER = argparse.ArgumentParser(description='Analyze temperature data.')
PARSER.add_argument('data_directory',
                    type=str,
                    help='the file location/name of the temperature data')
PARSER.add_argument('-fps',
                    type=int,
                    default=60,
                    required=False,
                    help='video framerate')
PARSER.add_argument('-scale',
                    type=int,
                    default=1,
                    required=False,
                    help='int factor to scale output videos by')
PARSER.add_argument(
    '-fcontour',
    type=int,
    default=False,
    required=False,
    help=
    'integer specifying the number of pixels around the contour cog to focus the image on'
)
PARSER.add_argument(
    '-fmax',
    type=int,
    default=False,
    required=False,
    help=
    'integer specifying the number of pixels around the max temperature to focus the image on'
)
PARSER.add_argument(
    '-cthresh',
    type=int,
    default=0,
    required=False,
    help='Integer specifying the threshold to draw contours from')
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
    '-cData',
    type=int,
    default=False,
    required=False,
    help='0 or 1 specifying wether or not to add contour data onto the video')

ARGS = PARSER.parse_args()

DATA_DIRECTORY = ARGS.data_directory
SCALE_FACTOR = ARGS.scale
FPS = ARGS.fps
REMOVE_TOP_REFLECTION = bool(ARGS.top)
REMOVE_BOTTOM_REFLECTION = bool(ARGS.bot)
FOLLOW_MAX = ARGS.fmax
FOLLOW_CONTOUR = ARGS.fcontour
CONTOUR_THRESHOLD = ARGS.cthresh
CDATA = bool(ARGS.cData)

DATASET = dset(DATA_DIRECTORY, REMOVE_TOP_REFLECTION, REMOVE_BOTTOM_REFLECTION)
VIEWER = np_vid_viewer.data_video(DATASET,
                                  ARGS.mp,
                                  follow_max_temp=FOLLOW_MAX,
                                  contour_threshold=CONTOUR_THRESHOLD,
                                  follow_contour=FOLLOW_CONTOUR,
                                  contour_data_on_img=CDATA)

VIEWER.save_video(SCALE_FACTOR, FPS)
