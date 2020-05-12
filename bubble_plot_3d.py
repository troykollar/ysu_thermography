import math

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from np_vid_viewer.helper_functions import printProgressBar


def plotBubble(temp_data: np.ndarray,
               pixel: tuple,
               threshold=200,
               start_frame=0,
               end_frame=-1,
               frame_count=-1):

    if start_frame == 0:
        if frame_count == -1 and end_frame == -1:
            frame_count = temp_data.shape[0]
        elif end_frame != -1:
            frame_count = end_frame - start_frame
        elif frame_count != -1:
            frame_count = frame_count

    else:
        if frame_count == -1 and end_frame == -1:
            frame_count = temp_data.shape[0] - start_frame
        elif end_frame != -1:
            frame_count = end_frame - start_frame
        elif frame_count != -1:
            frame_count = frame_count

    pixel_grad_mag = []
    pixel_grad_dir = []
    pixel_temp = []
    pixel_frame = []

    for i in range(frame_count):
        printProgressBar(i, frame_count)
        temp = temp_data[i + start_frame].copy()
        gradientx, gradienty = np.gradient(temp)

        if temp[pixel] > threshold:
            #print(temp[pixel])
            pixel_frame.append(i + start_frame)
            pixel_grad_mag.append(
                math.sqrt((gradientx[pixel]**2) + (gradienty[pixel]**2)))
            pixel_temp.append(temp[pixel])
            if gradientx[pixel] == 0:
                if gradienty[pixel] > 0:
                    pixel_grad_dir.append(90)
                elif gradienty[pixel] < 0:
                    pixel_grad_dir.append(-90)
                else:
                    pixel_grad_dir.append(0)
            else:
                pixel_grad_dir.append(
                    (180 / math.pi) *
                    math.atan(gradienty[pixel] / gradientx[pixel]))
    """
    print(len(np.asarray(pixel_temp).flatten()))
    print(len(np.asarray(pixel_grad_mag).flatten()))
    print(len(np.asarray(pixel_grad_dir).flatten()))
    """
    fig = go.Figure(
        data=go.Scatter3d(x=np.asarray(pixel_frame).flatten(),
                          y=np.asarray(pixel_grad_mag).flatten(),
                          z=np.asarray(pixel_grad_dir).flatten(),
                          text=np.asarray(pixel_temp).flatten(),
                          mode="markers",
                          marker=dict(color=np.asarray(pixel_temp).flatten(),
                                      size=5,
                                      colorbar_title='Temperature')))

    fig.update_layout(height=1000,
                      width=1000,
                      title='Pixel Temp and Gradient Magnitude and Angle',
                      scene=dict(xaxis=dict(title='Frame'),
                      yaxis=dict(title='Gradient Magnitude'),
                      zaxis=dict(title='Gradient Angle')))

    fig.show()


'''
plotBubble(np.load('/home/rjyarwood/Documents/Research/ResearchData/4-20_part_merged_data/thermal_cam_temps.npy'),
           pixel=(5, 88),
           threshold=500)
'''
