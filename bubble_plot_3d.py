import math

import plotly.graph_objects as go
import numpy as np
import pandas as pd


def plotBubble(temp_file, pixel, threshold=200, frame_count=-1):
    temp_data = np.load(temp_file, allow_pickle=True)

    if frame_count == -1:
        frame_count = temp_data.shape[0]

    pixel_grad_mag = []
    pixel_grad_dir = []
    pixel_temp = []

    for i in range(frame_count):
        temp = temp_data[i].copy()
        gradientx, gradienty = np.gradient(temp)
        if temp[pixel] > threshold:
            print(temp[pixel])
            pixel_grad_mag.append(math.sqrt((gradientx[pixel] ** 2) + (gradienty[pixel] ** 2)))
            pixel_temp.append(temp)
            if gradientx[pixel] == 0:
                if gradienty[pixel] > 0:
                    pixel_grad_dir.append(90)
                elif gradienty[pixel] < 0:
                    pixel_grad_dir.append(-90)
                else:
                    pixel_grad_dir.append(0)
            else:
                pixel_grad_dir.append((180 / math.pi) * math.atan(gradienty[pixel] / gradientx[pixel]))

    print(len(pixel_temp))
    print(len(pixel_grad_dir))
    print(len(pixel_grad_mag))
    fig = go.Figure(data=go.Scatter3d(
        x=pixel_temp,
        y=pixel_grad_mag,
        z=pixel_grad_dir,
        mode="markers",
        marker=dict(
            size=6,
            color='red'
        )
    ))

    fig.update_layout(height=800, width=800,
                      title='Pixel Temp and Gradient Magnitude and Angle')

    fig.show()


plotBubble('/home/rjyarwood/Documents/Research/ResearchData/4-8_part_merged_data/thermal_cam_temps.npy',
           pixel=(5, 88),
           threshold=500)
