import numpy as np
import os
import matplotlib.pyplot as plt
# from matplotlib.widgets import Cursor, Button
from math import sqrt


def histogram_generation(data, start_frame, end_frame, pixel, bins):

    temps = np.load(data + "/thermal_cam_temps.npy", mmap_mode='r')

    if end_frame <= 0 or end_frame > temps.shape[0]:
        end_frame = temps.shape[0]

    if start_frame < 0:
        start_frame = 0

    if end_frame < start_frame:
        start_frame, end_frame = end_frame, start_frame

    vid_frames = np.arange(start_frame, end_frame - start_frame)

    # Magnitude arrays
    x_mag = []
    y_mag = []

    # Angle array
    angle_arr = []

    x, y = np.shape(temps[0, :, :])
    xr = np.arange(x)  # Set span of x-axis for meshgrid
    yr = np.arange(y)  # Set span of y-axis for meshgrid
    xg, yg = np.meshgrid(yr, xr)

    for frame_index in vid_frames:
        data = temps[frame_index, :, :]
        result_matrix = np.asmatrix(data)
        dy, dx = np.gradient(result_matrix)  # Retrieve image gradient data

        x_magnitude = dx[pixel]  # Pixel magnitude W.R.T. x-axis
        y_magnitude = dy[pixel]  # Pixel magnitude W.R.T. y-axis
        angle = sqrt((x_magnitude ** 2) + (y_magnitude ** 2))  # Gradient angle formula

        x_mag.append(x_magnitude)  # store pixel x-magnitude for fram in array
        y_mag.append(y_magnitude)  # store pixel y-magnitude for fram in array
        angle_arr.append(angle)  # store pixel angle for fram in array

    # Plotting----------------------------------------------------------------------
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle('Pixel ({},{}) Temperature Data'.format(pixel[0], pixel[1]))

    # X-magnitude plot
    xmag_minimum = np.amin(x_mag)
    xmag_maximum = np.amax(x_mag)
    ax1.set_xlabel('X-Direction Magnitude')
    ax1.set_ylabel('Frequency')
    ax1.hist(x_mag, bins=bins, range=(xmag_minimum, xmag_maximum), edgecolor='black')

    # Y-magnitude plot
    ymag_minimum = np.amin(y_mag)
    ymag_maximum = np.amax(y_mag)
    ax2.set_xlabel('Y-Direction Magnitude')
    ax2.set_ylabel('Frequency')
    ax2.hist(y_mag, bins=bins, range=(ymag_minimum, ymag_maximum), edgecolor='black')

    # Angle plot
    angle_minimum = np.amin(angle_arr)
    angle_maximum = np.amax(angle_arr)
    ax3.set_xlabel('Angle')
    ax3.set_ylabel('Frequency')
    ax3.hist(angle_arr, bins=bins, range=(angle_minimum, angle_maximum), edgecolor='black')
    plt.show()
