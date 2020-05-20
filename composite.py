"""Functions to generate composite images and videos for thermal data analysis"""
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import printProgressBar
from dataset import DataSet, get_dataset_CLargs


def increment_from_thresh(img: np.ndarray, data_frame: np.ndarray,
                          threshold: int):
    over_thresh_array = cv2.threshold(data_frame, threshold, 1,
                                      cv2.THRESH_BINARY)
    over_thresh_array = over_thresh_array[1]
    img += over_thresh_array


def get_threshold_img(dataset: DataSet,
                      threshold: int,
                      start=-1,
                      end=-1,
                      cap=None):
    # Get frame size info
    height = dataset[0].shape[0]
    width = dataset[0].shape[1]

    # TODO: Add better validation for start and end frames
    final_frame = dataset.shape[0]
    if end < 0 or end > final_frame:
        end = final_frame
    else:
        end = end + 1

    if start < 0 or start > final_frame:
        start = 0

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    for i in range(start, end):
        printProgressBar(i - start, end - start,
                         "Generating threshold image...")
        frame = dataset[i]
        increment_from_thresh(threshold_img, frame, threshold)

    if cap is not None:
        over_cap = np.where(threshold_img > cap)
        for y, x in zip(over_cap[0], over_cap[1]):
            threshold_img[y, x] = cap

    return threshold_img


def save_threshold_img(filename: str,
                       threshold_img: np.ndarray,
                       threshold: int,
                       dst_folder=None):
    # Get temp data info
    build_folder = filename[:filename.rfind('/')]
    build_number = build_folder[:build_folder.find('_')]
    build_number = build_number[(build_number.rfind('/') + 1):]

    # If a dst folder is not entered, dst folder is the build folder
    if dst_folder is None:
        dst_folder = build_folder

    # Generate a filename based on build_number and threshold used
    save_filename = filename = dst_folder + '/' + build_number + '_threshold' + str(
        threshold) + '.png'
    raw_filename = filename = dst_folder + '/' + build_number + '_threshold' + str(
        threshold) + '_raw.png'

    fig, ax = plt.subplots()
    fig.suptitle('Build: ' + str(build_number) + ' Threshold: ' +
                 str(threshold))
    im = ax.imshow(threshold_img, cmap='inferno')
    cbar = ax.figure.colorbar(im,
                              ax=ax,
                              label='Number of frames above ' + str(threshold))

    plt.imsave(raw_filename, threshold_img, cmap='inferno')

    plt.savefig(save_filename)
    plt.close()
    print('\n')
    print('Threshold img saved as: ' + filename)


def get_composite_CLargs(parser: argparse.ArgumentParser):
    """Add composite related CL arguments to given parser.

    Added Arguments
    ---------------
    THRESHOLD: required
        int specifying the threshold to be used for the composite image.
    dst_folder: optional
        str specifying where to save the composite image. Defaults to build folder.
    cap: optional
        int specifying the max number of frames to use for composite.
    start: optional
        int specifying the first frame to consider for the composite.
    end: optional
        int specifying the last frame to consider for the composite.
    debug: optional
        0 or 1 specifying whether to show each frame being used for the composite.
    """
    parser.add_argument('THRESHOLD',
                        type=int,
                        help='temperature theshold of the image')
    parser.add_argument('-dst_folder',
                        type=str,
                        default=None,
                        help='Destination folder to save composite image.')
    parser.add_argument('-cap',
                        type=int,
                        help='Maximum number of frames to increment')
    parser.add_argument('-start',
                        type=int,
                        default=-1,
                        required=False,
                        help='First frame to consider.')
    parser.add_argument('-end',
                        type=int,
                        default=-1,
                        required=False,
                        help='Last frame to consider.')
    parser.add_argument(
        '-debug',
        type=int,
        default=False,
        help='Show each frame composite is using to generate from.')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Generate a composite image.')

    get_dataset_CLargs(arg_parser)
    get_composite_CLargs(arg_parser)

    args = arg_parser.parse_args()

    temp_data = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    composite_threshold = args.THRESHOLD

    destination_folder = args.dst_folder
    frame_cap = args.cap
    start_frame = args.start
    end_frame = args.end
    debug = bool(args.debug)

    data_set = DataSet(temp_data,
                       remove_top_reflection=top,
                       remove_bottom_reflection=bot)
    thresh_img = get_threshold_img(dataset=data_set,
                                   threshold=composite_threshold,
                                   start=start_frame,
                                   end=end_frame,
                                   cap=frame_cap)
    save_threshold_img(filename=temp_data,
                       threshold_img=thresh_img,
                       threshold=composite_threshold,
                       dst_folder=destination_folder)
