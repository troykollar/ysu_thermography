import math

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from np_vid_viewer.helper_functions import printProgressBar


def plotBubble(temp_data: np.ndarray,
               pixel: tuple,
               threshold: int,
               start_frame=0,
               end_frame=-1,
               frame_count=-1):



    pixel_grad_mag = []
    pixel_grad_dir = []
    pixel_temp = []
    pixel_frame = []

    for i in range(frame_count):
        printProgressBar(i, frame_count)
        temp = temp_data[i + start_frame].copy()

        if temp[pixel] > threshold:

            result_matrix = np.asmatrix(temp)

            dy, dx = np.gradient(result_matrix)  # Retrieve image gradient data
            x_dir = dx[pixel]  # Pixel magnitude W.R.T. x-axis
            y_dir = dy[pixel]  # Pixel magnitude W.R.T. y-axis

            # Magnitude Calculation
            magnitude = math.sqrt((x_dir**2) + (y_dir**2))

            # Angle Calculation
            angle_rad = (np.arctan2(y_dir, x_dir) - (math.pi / 2)
                         )  # shift -90 deg
            angle_deg = (angle_rad * (180 / math.pi))  # Convert to degrees

            pixel_frame.append(i + start_frame)
            pixel_grad_mag.append(magnitude)
            pixel_temp.append(temp[pixel])
            pixel_grad_dir.append(angle_deg)
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
                      title='Pixel Temp and Gradient Magnitude and Angle for: ' + str(pixel) + ' Threshold: ' + str(threshold),
                      scene=dict(xaxis=dict(title='X: Frame'),
                                 yaxis=dict(title='Y: Gradient Magnitude'),
                                 zaxis=dict(title='Z: Gradient Angle')))

    fig.show()



plotBubble(np.load('/home/rjyarwood/Documents/Research/ResearchData/4-20_part_merged_data/thermal_cam_temps.npy'),
           pixel=(5, 88),
           threshold=500)

