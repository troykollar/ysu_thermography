import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
# import datetime


def contourVidGen(data, start_frame, end_frame, contour_levels, fps, video_name):

    temps = np.load(data + "/thermal_cam_temps.npy", mmap_mode='r')

    if end_frame <= 0 or end_frame > temps.shape[0]:
        end_frame = temps.shape[0]

    if start_frame < 0:
        start_frame = 0

    if end_frame < start_frame:
        start_frame, end_frame = end_frame, start_frame

    vid_frames = np.arange(start_frame, end_frame - start_frame)

    fig, ax = plt.subplots()
    x, y = np.shape(temps[0, :, :])
    xr = np.arange(x)
    yr = np.arange(y)

    for frame_index in vid_frames:
        plt.clf()
        # make figure w/o frame
        fig = plt.figure(frameon=False)
        fig.set_size_inches(6, 4)  # set figure size (inches)
        # Make content fill whole figure
        ax = plt.Axes(fig, [0, 0, 1, 1])  # left, bottom, width, height normalized dimensions
        ax.set_axis_off()
        fig.add_axes(ax)

        # draw image on figure
        c = ax.contourf(yr, -xr, temps[frame_index, :, :], levels=contour_levels, cmap='inferno')
        cbar = plt.colorbar(c, shrink=0.75, extend='both')

        # save fig
        fname = 'Frame' + str(frame_index) + '.png'
        fig.savefig(fname, transparent=True)
        plt.close()

    images = [img for img in os.listdir(data) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(data, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(data, image)))
        os.remove(image)

    cv2.destroyAllWindows()
    video.release()
    print('DONE')
