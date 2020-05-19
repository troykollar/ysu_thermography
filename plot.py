import math
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import printProgressBar
from dataset import DataSet


class Plots:
    def __init__(self,
                 temp_data: DataSet,
                 pixel: tuple,
                 threshold: int,
                 start_frame=0,
                 end_frame=-1,
                 frame_count=-1):

        self.grid_lines = True
        self.data = temp_data
        self.pixel = pixel
        self.threshold = threshold
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame_count = frame_count
        self.cartesianPixel = (pixel[1], pixel[0])

        self.frames = []
        self.x_magnitude_array = []
        self.y_magnitude_array = []
        self.magnitude_array = []
        self.angle_array = []
        self.temperatures_array = []

        self.angle_deg_minimum = None
        self.angle_deg_maximum = None
        self.mag_minimum = None
        self.mag_maximum = None
        self.binning1 = None
        self.binning2 = None

        self.fixFrameCounts()
        self.gradientMath()
        self.calculateBins()

    def all(self):
        self.plot3DBubble()
        self.plotAngle()
        self.plotMagnitude()
        self.plotScatter()
        self.plotHexBin()
        self.plot2DHistogram()

    def fixFrameCounts(self):
        if self.start_frame == 0:
            if self.frame_count == -1 and self.end_frame == -1:
                self.frame_count = self.data.shape[0]
            elif self.end_frame != -1:
                self.frame_count = self.end_frame - self.start_frame
            elif self.frame_count != -1:
                self.frame_count = self.frame_count

        else:
            if self.frame_count == -1 and self.end_frame == -1:
                self.frame_count = self.data.shape[0] - self.start_frame
            elif self.end_frame != -1:
                self.frame_count = self.end_frame - self.start_frame
            elif self.frame_count != -1:
                self.frame_count = self.frame_count

    def gradientMath(self):

        for frame_index in range(self.frame_count):
            printProgressBar(frame_index, self.frame_count)

            temp = self.data[frame_index + self.start_frame]
            result_matrix = np.asmatrix(temp)

            if temp[self.pixel] > self.threshold:
                dy, dx = np.gradient(
                    result_matrix)  # Retrieve image gradient data
                x_dir = dx[self.pixel]  # Pixel magnitude W.R.T. x-axis
                y_dir = dy[self.pixel]  # Pixel magnitude W.R.T. y-axis

                # Magnitude Calculation
                magnitude = math.sqrt((x_dir**2) + (y_dir**2))

                # Angle Calculation
                angle_rad = (np.arctan2(y_dir, x_dir) - (math.pi / 2)
                             )  # shift -90 deg
                angle_deg = (angle_rad * (180 / math.pi))  # Convert to degrees

                self.x_magnitude_array.append(
                    x_dir)  # store pixel x-direction for frame in array
                self.y_magnitude_array.append(
                    y_dir)  # store pixel y-direction for frame in array
                self.magnitude_array.append(
                    magnitude)  # store pixel magnitude for frame in array
                self.angle_array.append(
                    angle_deg)  # store pixel angle for frame in array
                self.temperatures_array.append(temp[self.pixel])
                self.frames.append(frame_index + self.start_frame)

    def calculateBins(self):
        self.angle_deg_minimum = np.amin(self.angle_array)
        self.angle_deg_maximum = np.amax(self.angle_array)
        self.mag_minimum = np.amin(self.magnitude_array)
        self.mag_maximum = np.amax(self.magnitude_array)
        self.binning1 = int((abs(self.mag_maximum - self.mag_minimum)) / 5)
        self.binning2 = int(self.binning1 / 1.5)

    def plot3DBubble(self):
        fig = go.Figure(data=go.Scatter3d(
            x=np.asarray(self.frames).flatten(),
            y=np.asarray(self.magnitude_array).flatten(),
            z=np.asarray(self.angle_array).flatten(),
            text=np.asarray(self.temperatures_array).flatten(),
            mode="markers",
            marker=dict(color=np.asarray(self.temperatures_array).flatten(),
                        size=5,
                        colorbar_title='Temperature')))
        fig.update_layout(
            height=1000,
            width=1000,
            title='Pixel Temp and Gradient Magnitude and Angle for: ' +
            str(self.cartesianPixel) + ' Threshold: ' + str(self.threshold),
            scene=dict(xaxis=dict(title='X: Frame'),
                       yaxis=dict(title='Y: Gradient Magnitude'),
                       zaxis=dict(title='Z: Gradient Angle')))
        fig.show()

    def plotMagnitude(self):
        # Plotting
        # Magnitude plot
        fig1, ax1 = plt.subplots()
        fig1.suptitle(
            'Pixel {} Magnitude Histogram:\n{} Bins, Threshold: {}'.format(
                self.cartesianPixel, self.binning1, self.threshold))
        ax1.set_xlabel('Magnitude (sqrt(x^2+y^2))')
        ax1.set_ylabel('Frequency')
        ax1.hist(self.magnitude_array,
                 bins=self.binning1,
                 range=(self.mag_minimum, self.mag_maximum),
                 edgecolor='black')
        ax1.grid(b=self.grid_lines, which='major', alpha=0.3)

    def plotAngle(self):
        # Angle plot - degrees
        fig2, ax2 = plt.subplots()
        fig2.suptitle(
            'Pixel {} Angle Histogram:\n{} Bins, Threshold: {}\n'.format(
                self.cartesianPixel, self.binning2, self.threshold))
        ax2.set_xlabel('Angle (°)')
        ax2.set_ylabel('Frequency')
        counts, bins, bars = ax2.hist(self.angle_array,
                                      bins=self.binning2,
                                      range=(self.angle_deg_minimum,
                                             self.angle_deg_maximum),
                                      edgecolor='black')
        ax2.grid(b=self.grid_lines, which='major', alpha=0.3)

    def plot2DHistogram(self):
        #2D Histogram - Magnitude vs Angle (degrees)
        histgrid = (self.binning1, self.binning2)
        fig3, ax3 = plt.subplots()
        fig3.suptitle(
            'Pixel {} Magnitude vs Angle Histogram:\nThreshold: {}\n'.format(
                self.cartesianPixel, self.threshold))
        ax3.set_xlabel('Angle (°)')
        ax3.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        histplot = ax3.hist2d(self.angle_array,
                              self.magnitude_array,
                              bins=histgrid,
                              cmap='gnuplot')
        ax3.grid(b=self.grid_lines, which='major', alpha=0.3)
        plt.colorbar(histplot[3])

    def plotScatter(self):
        # Scatterplot - Magnitude vs Angle (degrees)
        fig4, ax4 = plt.subplots()
        fig4.suptitle(
            'Pixel {} Magnitude vs Angle Scatterplot:\nThreshold: {}\n'.format(
                self.cartesianPixel, self.threshold))
        ax4.set_xlabel('Angle (°)')
        ax4.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        ax4.scatter(self.angle_array, self.magnitude_array)
        ax4.grid(b=self.grid_lines, which='major', alpha=0.3)

    def plotHexBin(self):
        # "Hexbin plot" - Magnitude vs Angle (degrees)
        hexgrid = (self.binning1, self.binning2)
        fig5, ax5 = plt.subplots()
        fig5.suptitle(
            'Pixel {} Magnitude and Angle Hist:\nThreshold: {}\n'.format(
                self.cartesianPixel, self.threshold))
        ax5.set_xlabel('Angle (°)')
        ax5.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        hexplot = ax5.hexbin(self.angle_array,
                             self.magnitude_array,
                             gridsize=hexgrid,
                             cmap='gnuplot')
        ax5.grid(b=self.grid_lines, which='major', alpha=0.3)
        plt.colorbar(hexplot)

        plt.show()
