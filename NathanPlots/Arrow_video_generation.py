import numpy as np
import os
import matplotlib.pyplot as plt
import cv2


def contourVidGen(data, start_frame, end_frame, fps, video_name):
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
    xg, yg = np.meshgrid(yr, xr)

    skip = (slice(None, None, 2), slice(None, None, 2))  # sets amount of arrows shown

    for frame_index in vid_frames:
        data = temps[frame_index, :, :]
        result_matrix = np.asmatrix(data)
        dy, dx = np.gradient(result_matrix)
        plt.clf()

        # make figure w/o frame
        fig = plt.figure(frameon=False)
        fig.set_size_inches(8.5, 6.25)  # set figure size (inches)

        # Make content fill whole figure
        ax = plt.Axes(fig, [0, 0, 1, 1])  # left, bottom, width, height normalized dimensions
        ax.set_axis_off()
        fig.add_axes(ax)


        # draw image on figure
        def func_to_vectorize(x, y, dx, dy, scaling=1):
            plt.arrow(x, y, dx * scaling, dy * scaling, fc="k", ec="k", head_width=0.5,
                      head_length=0.5)  # scales arrow size


        vectorized_arrow_drawing = np.vectorize(func_to_vectorize)
        plt.imshow(result_matrix, cmap="inferno")
        vectorized_arrow_drawing(xg[skip], yg[skip], -dx[skip], -dy[skip], 0.02)  # scale of vector magnitude
        plt.colorbar(shrink=0.75)

        # save fig
        fname = 'Frame' + str(frame_index) + '.png'
        fig.savefig(fname, transparent=True)
        plt.close()

    # video generation
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