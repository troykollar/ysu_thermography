"""Functions to generate composite images and videos for thermal data analysis"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import np_vid_viewer.progress_bar as progress_bar


def generate_threshold_image(temp_filename: str,
                             threshold=800,
                             start=0,
                             end=0):
    """Saves a 16 bit threshold image

    Each pixel of the resulting image is incremented every time the temperature at that pixel is
    above the temperature threshold.

    Parameters
    ----------
    temp_filename : str
        Filename including location of the thermal_cam_temps.npy file.
    threshold : int
        Temperature threshold which determines if a pixel will be incremented.

    """
    # Get temp data info
    temp_data = np.load(temp_filename, mmap_mode="r", allow_pickle=True)
    build_folder = temp_filename[:temp_filename.rfind('/')]
    build_number = build_folder[:build_folder.find('_')]
    build_number = build_number[(build_number.rfind('/') + 1):]

    # Get frame info
    num_frames = temp_data.shape[0]
    height = temp_data[0].shape[0]
    width = temp_data[0].shape[1]

    if end == 0:
        end = num_frames - 1

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    # Check each pixel, if pixel is over threshold, increment that pixel in theshold_img
    for i, frame in enumerate(temp_data[start:end]):
        # Show progress
        progress_bar.printProgressBar(i,
                                      num_frames,
                                      prefix='Generating threshold image...')
        over_thresh_array = cv2.inRange(frame, threshold, int(np.amax(frame)))

        threshold_img += over_thresh_array

    # Generate a filename based on build_number and threshold used
    filename = build_folder + '/' + build_number + '_threshold' + str(
        threshold) + '.png'
    plt.imsave(filename, threshold_img, cmap='inferno')
    print('Threshold img saved as: ' + filename)
