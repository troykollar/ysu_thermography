import numpy as np
import os
import matplotlib.pyplot as plt
import math
from np_vid_viewer.helper_functions import printProgressBar


def get_visualization(temp_data: np.ndarray,
                      path: str,
                      pixel: tuple,
                      threshold: int,
                      start_frame=-1,
                      end_frame=-1,
                      gridlines=True):

    pixel_x = pixel[0]
    pixel_y = pixel[1]

    if start_frame < 0:
        start_frame = 0

    if end_frame < 0:
        end_frame = temp_data.shape[0]

    #directory = os.chdir(path)
    temps = temp_data
    vid_frames = np.arange(start_frame, end_frame)

    #Direction arrays
    x_mag = []
    y_mag = []

    #Angle array
    angle_arr_deg = []

    #Magnitude array
    mag_arr = []

    #Storage array
    record = []

    for frame_index in vid_frames:
        printProgressBar(frame_index, vid_frames[-1])

        # Possible bug, I think numpy arrays are read y,x instead of x,y
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
            angle_deg = (angle_rad * (180 / math.pi))  #Convert to degrees

            x_mag.append(x_dir)  #store pixel x-direction for frame in array
            y_mag.append(y_dir)  #store pixel y-direction for frame in array
            mag_arr.append(
                magnitude)  #store pixel magnitude for frame in array
            angle_arr_deg.append(
                angle_deg)  #store pixel angle for frame in array

    data_points = len(record)

    # Original code, but removed because angle_arr_rad is undefined
    #if not (x_mag or y_mag or mag_arr or angle_arr_rad or angle_arr_deg):
    if not (x_mag or y_mag or mag_arr or angle_arr_deg):
        print('Data array is empty!')
        print(
            'There are {} data points above threshold of {} within frames {} to {}'
            .format(data_points, threshold, start_frame, end_frame))

    else:
        #Plotting
        #Magnitude plot
        mag_minimum = np.amin(mag_arr)
        mag_maximum = np.amax(mag_arr)
        binning1 = int((abs(mag_maximum - mag_minimum)) / 5)
        fig1, ax1 = plt.subplots()
        fig1.suptitle(
            'Pixel ({},{}) Magnitude Histogram:\n{} Bins, Threshold: {}'.
            format(pixel_x, pixel_y, binning1, threshold))
        ax1.set_xlabel('Magnitude (sqrt(x^2+y^2))')
        ax1.set_ylabel('Frequency')
        ax1.hist(mag_arr,
                 bins=binning1,
                 range=(mag_minimum, mag_maximum),
                 edgecolor='black')
        ax1.grid(b=gridlines, which='major', alpha=0.3)

        #Angle plot - degrees
        angle_deg_minimum = np.amin(angle_arr_deg)
        angle_deg_maximum = np.amax(angle_arr_deg)
        binning2 = int(binning1 / 1.5)
        fig2, ax2 = plt.subplots()
        fig2.suptitle(
            'Pixel ({},{}) Angle Histogram:\n{} Bins, Threshold: {}\n'.format(
                pixel_x, pixel_y, binning2, threshold))
        ax2.set_xlabel('Angle (°)')
        ax2.set_ylabel('Frequency')
        counts, bins, bars = ax2.hist(angle_arr_deg,
                                      bins=binning2,
                                      range=(angle_deg_minimum,
                                             angle_deg_maximum),
                                      edgecolor='black')
        ax2.grid(b=gridlines, which='major', alpha=0.3)

        #2D Histogram - Magnitude vs Angle (degrees)
        histgrid = (binning1, binning2)
        fig3, ax3 = plt.subplots()
        fig3.suptitle(
            'Pixel ({},{}) Magnitude vs Angle Histogram:\nThreshold: {}\n'.
            format(pixel_x, pixel_y, threshold))
        ax3.set_xlabel('Angle (°)')
        ax3.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        histplot = ax3.hist2d(angle_arr_deg,
                              mag_arr,
                              bins=histgrid,
                              cmap='gnuplot')
        ax3.grid(b=gridlines, which='major', alpha=0.3)
        plt.colorbar(histplot[3])

        #Scatterplot - Magnitude vs Angle (degrees)
        fig4, ax4 = plt.subplots()
        fig4.suptitle(
            'Pixel ({},{}) Magnitude vs Angle Scatterplot:\nThreshold: {}\n'.
            format(pixel_x, pixel_y, threshold))
        ax4.set_xlabel('Angle (°)')
        ax4.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        ax4.scatter(angle_arr_deg, mag_arr)
        ax4.grid(b=gridlines, which='major', alpha=0.3)

        #"Hexbin plot" - Magnitude vs Angle (degrees)
        hexgrid = (binning1, binning2)
        fig5, ax5 = plt.subplots()
        fig5.suptitle(
            'Pixel ({},{}) Magnitude and Angle Hist:\nThreshold: {}\n'.format(
                pixel_x, pixel_y, threshold))
        ax5.set_xlabel('Angle (°)')
        ax5.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        hexplot = ax5.hexbin(angle_arr_deg,
                             mag_arr,
                             gridsize=hexgrid,
                             cmap='gnuplot')
        ax5.grid(b=gridlines, which='major', alpha=0.3)
        plt.colorbar(hexplot)

        plt.show()

        hottest = np.amax(record)
        print('Data for frame {} to {}'.format(start_frame, end_frame))
        print('Number of data points above {}: {}'.format(
            threshold, data_points))
        print('Highest Value: {}'.format(hottest))