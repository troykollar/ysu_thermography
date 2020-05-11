"""

Creates a historgram for (a) given pixel(s) gradient magnitude taking the pixel location, the temp threshold to skip anything below and the bin resolution

"""
import np_vid_viewer
import numpy as np
import matplotlib.pyplot as plt
import math


def plotHistogram(temp_file, pixel, threshold=200, binCount=5, spacing=1):
    temp_data = np.load(temp_file, allow_pickle=True)

    frame_count = temp_data.shape[0]
    pixel_grad_mag = []
    pixel_grad_dir = []

    for i in range(frame_count):
        temp = temp_data[i].copy()
        gradientx, gradienty = np.gradient(temp, spacing)
        if temp[pixel] > threshold:
            pixel_grad_mag.append(math.sqrt((gradientx[pixel] ** 2) + (gradienty[pixel] ** 2)))
            if gradientx[pixel] == 0:
                if gradienty[pixel] > 0:
                    pixel_grad_dir.append(90)
                elif gradienty[pixel] < 0:
                    pixel_grad_dir.append(-90)
                else:
                    pixel_grad_dir.append(0)
            else:
                pixel_grad_dir.append((180 / math.pi) * math.atan(gradienty[pixel] / gradientx[pixel]))

    n, bins, patches = plt.hist(pixel_grad_dir, binCount, facecolor='blue', alpha=.5)
    plt.xlabel('Gradient Angle')
    plt.ylabel('Frequency')
    plt.show()


def plotLine(temp_file, pixel, startFrame: int, endFrame: int):
    temp_data = np.load(temp_file, allow_pickle=True)
    if endFrame is -1:
        endFrame = temp_data.shape[0] - 1

    frame = np.arange(int(startFrame), int(endFrame))
    pixelTempHistory = temp_data[frame, int(pixel[0]), int(pixel[1])]

    plt.plot(frame, pixelTempHistory)
    plt.show()






