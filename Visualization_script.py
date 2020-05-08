import numpy as np
import os
import matplotlib.pyplot as plt
import math


def get_visualization(path,
                      pixel_x,
                      pixel_y,
                      data_list='thermal_cam_temps.npy',
                      start=None,
                      end=None,
                      bins=100,
                      threshold=100):
    path = path  #specify directory to look in
    data_list = data_list  #specify data set to look at
    if start is None:
        start_frame = 0
    else:
        start_frame = start
    if end is None:
        end_frame = 27000
    else:
        end_frame = end

    start_frame = 0  #specify which frame to begin at
    num_frame = 27000  #specify number of frames to look at

    directory = os.chdir(path)
    temps = np.load(data_list, mmap_mode='r')
    end_frame = start_frame + num_frame
    vid_frames = np.arange(start_frame, end_frame)

    #Direction arrays
    x_mag = []
    y_mag = []

    #Angle arrays
    angle_arr_rad = []
    angle_arr_deg = []

    #Magnitude array
    mag_arr = []

    #Storage array
    record = []

    for frame_index in vid_frames:
        print(str(frame_index) + '/' + str(vid_frames))

        pixel = temps[frame_index, pixel_x, pixel_y]
        data = temps[frame_index, :, :]
        result_matrix = np.asmatrix(data)

        if pixel > threshold:

            record.append(pixel)

            dy, dx = np.gradient(result_matrix)  #Retrieve image gradient data
            x_dir = dx[pixel_x, pixel_y]  #Pixel magnitude W.R.T. x-axis
            y_dir = dy[pixel_x, pixel_y]  #Pixel magnitude W.R.T. y-axis

            #Magnitude Calculation
            magnitude = math.sqrt((x_dir**2) + (y_dir**2))

            #Angle Calculation
            angle_rad = (np.arctan2(y_dir, x_dir) - (math.pi / 2)
                         )  #shift -90 deg
            angle_deg = (angle_rad * (180 / math.pi))

            x_mag.append(x_dir)  #store pixel x-direction for frame in array
            y_mag.append(y_dir)  #store pixel y-direction for frame in array
            mag_arr.append(
                magnitude)  #store pixel magnitude for frame in array
            angle_arr_rad.append(
                angle_rad)  #store pixel angle for frame in array
            angle_arr_deg.append(
                angle_deg)  #store pixel angle for frame in array

    #Plotting----------------------------------------------------------------------
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16, 12))
    fig.tight_layout()
    fig.suptitle(
        'Pixel ({},{}) Temperature Data: {} bins, Threshold {}'.format(
            pixel_x, pixel_y, bins, threshold))

    #Magnitude plot
    mag_minimum = np.amin(mag_arr)
    mag_maximum = np.amax(mag_arr)
    ax1.set_xlabel('Magnitude (sqrt(x^2+y^2))')
    ax1.set_ylabel('Frequency')
    ax1.hist(mag_arr,
             bins=bins,
             range=(mag_minimum, mag_maximum),
             edgecolor='black')

    #Angle plot - degrees
    angle_deg_minimum = np.amin(angle_arr_deg)
    angle_deg_maximum = np.amax(angle_arr_deg)
    ax2.set_xlabel('Angle (°)')
    ax2.set_ylabel('Frequency')
    ax2.hist(angle_arr_deg,
             bins=bins,
             range=(angle_deg_minimum, angle_deg_maximum),
             edgecolor='black')

    #2D Histogram - Magnitude vs Angle (degrees)
    ax3.set_xlabel('Angle (°)')
    ax3.set_ylabel('Magnitude (sqrt(x^2+y^2))')
    ax3.hist2d(angle_arr_deg, mag_arr, bins=(30, 20), cmap=plt.cm.Reds)

    #"Bubble Plot" - Magnitude vs Angle (degrees)
    ax4.set_xlabel('Angle (°)')
    ax4.set_ylabel('Magnitude (sqrt(x^2+y^2))')
    ax4.scatter(angle_arr_deg, mag_arr, alpha=0.5)

    plt.savefig('pixel' + str(pixel_x) + '-' + str(pixel_y) + '_visualization')

    data_points = len(record)
    hottest = np.amax(record)

    print('Data for frame {} to {}'.format(start_frame, end_frame))
    print('Number of data points above {}: {}'.format(threshold, data_points))
    print('Highest Value: {}'.format(hottest))