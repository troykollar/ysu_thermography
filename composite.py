"""Functions to generate composite images and videos for thermal data analysis"""
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from helper_functions import printProgressBar
from dataset import DataSet


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
    if end < 0 or end > dataset.final_frame:
        end = dataset.final_frame

    if start < 0 or start > dataset.final_frame:
        start = 0

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    for i, frame in enumerate(dataset[start:end]):
        printProgressBar(i - start, end - start,
                         "Generating threshold image...")
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a composite image.')
    parser.add_argument('temp_data',
                        type=str,
                        help='filename (and location) of temp data')
    parser.add_argument('THRESHOLD',
                        type=int,
                        help='temperature theshold of the image')
    parser.add_argument('-dst_folder',
                        type=str,
                        default=None,
                        help='Destination folder to save composite image.')
    parser.add_argument('-rm_refl',
                        type=int,
                        default=False,
                        help='Whether or not to remove reflections.')
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

    args = parser.parse_args()
    load_filename = '/home/troy/thermography/4-20_corrected/thermal_cam_temps.npy'
    dst_folder = '/home/troy/thermography/4-20_corrected/'

    dataset = DataSet(args.temp_data, bool(args.rm_refl), bool(args.rm_refl))
    threshold_img = get_threshold_img(dataset=dataset,
                                      threshold=args.THRESHOLD,
                                      start=args.start,
                                      end=args.end,
                                      cap=args.cap)
    save_threshold_img(filename=args.temp_data,
                       threshold_img=threshold_img,
                       threshold=args.THRESHOLD,
                       dst_folder=args.dst_folder)
