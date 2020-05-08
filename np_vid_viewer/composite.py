"""Functions to generate composite images and videos for thermal data analysis"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from np_vid_viewer.helper_functions import printProgressBar


def increment_from_thresh(img: np.ndarray, data_frame: np.ndarray,
                          threshold: int):
    over_thresh_array = cv2.threshold(data_frame, threshold, 1,
                                      cv2.THRESH_BINARY)
    over_thresh_array = over_thresh_array[1]
    img += over_thresh_array


def get_threshold_img(dataset: np.ndarray,
                      threshold: int,
                      start=0,
                      end=0,
                      cap=None,
                      show_progress=False):
    # Get frame size info
    height = dataset[0].shape[0]
    width = dataset[0].shape[1]
    last_frame = dataset.shape[0]

    if end <= 0 or end >= last_frame:
        end = last_frame
    else:
        end = end + 1

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    # Check each pixel, if pixel is over threshold, increment that pixel in theshold_img
    start_time = time.time()
    for i, frame in enumerate(dataset[start:end]):
        if show_progress:
            printProgressBar(i - start, end - start, start_time,
                             "Generating threshold image...")
        increment_from_thresh(threshold_img, frame, threshold)

    if cap is not None:
        over_cap = np.where(threshold_img > cap)
        for y, x in zip(over_cap[0], over_cap[1]):
            threshold_img[y, x] = cap

    return threshold_img


def save_threshold_img(filename: str,
                       threshold: int,
                       dst_folder=None,
                       start=0,
                       end=0,
                       cap=None,
                       show_progress=False):
    # Get temp data info
    temp_data = np.load(filename, mmap_mode="r", allow_pickle=True)
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

    threshold_img = get_threshold_img(temp_data, threshold, start, end, cap,
                                      show_progress)

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
