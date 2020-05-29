import math
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import printProgressBar
from dataset import DataSet


class Plots:
    def __init__(self,
                 temp_data: DataSet,
                 pixels: list,
                 threshold: int,
                 start_frame=0,
                 end_frame=-1,
                 frame_count=-1,
                 relativeLoc: list = [],
                 gui_instance=None):

        self.gui_instance = gui_instance
        self.grid_lines = True
        self.data = temp_data

        self.pixels = []
        for pixel in pixels:
            self.pixels.append((pixel[1], pixel[0]))

        self.plotted_pixels = []
        self.temp_data = temp_data
        self.threshold = threshold
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame_count = frame_count
        self.cartesianPixel = pixel
        self.relativeLoc = relativeLoc

        self.frames = []
        self.x_magnitude_array = []
        self.y_magnitude_array = []
        self.magnitude_array = []
        self.angle_array = []
        self.temperatures_array = []

        self.angle_deg_minimum = []
        self.angle_deg_maximum = []
        self.mag_minimum = []
        self.mag_maximum = []
        self.binning1 = []
        self.binning2 = []

        #self.fixFrameCounts()
        self.gradientMath()
        self.calculateBins()

    def all(self):
        self.plot3DBubble()
        self.plotAngle()
        self.plotMagnitude()
        self.plotScatter()
        self.plotHexBin()
        self.plot2DHistogram()
        self.plotLine()

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

        if self.gui_instance is not None:
            self.gui_instance.create_progress_bar()

        for pixel in self.pixels:
            cur_pixel_x_mags = []
            cur_pixel_y_mags = []
            cur_pixel_mags = []
            cur_pixel_angles = []
            cur_pixel_temps = []
            cur_pixel_frames = []
            for i, frame in enumerate(self.temp_data):
                # Show progress bars
                printProgressBar(i, self.temp_data.end_frame)
                if self.gui_instance is not None:
                    self.gui_instance.update_progress_bar(
                        i, self.temp_data.end_frame)

                result_matrix = np.asmatrix(frame)

                # Retrieve image gradient data
                if frame[pixel] > self.threshold:
                    dy, dx = np.gradient(result_matrix)
                    x_dir = dx[pixel]
                    y_dir = dy[pixel]

                    # Magnitude Calculation
                    magnitude = math.sqrt((x_dir**2) + (y_dir**2))

                    # Angle Calculation
                    angle_rad = (np.arctan2(x_dir, y_dir) - (math.pi / 2)
                                 )  # shift -90 deg
                    angle_deg = (angle_rad * (180 / math.pi)
                                 )  # Convert to degrees

                    cur_pixel_x_mags.append(x_dir)
                    cur_pixel_y_mags.append(y_dir)
                    cur_pixel_mags.append(magnitude)
                    cur_pixel_angles.append(angle_deg)
                    cur_pixel_frames.append(i + self.temp_data.start_frame)
                    cur_pixel_temps.append(frame[pixel])

            if cur_pixel_frames:
                self.x_magnitude_array.append(cur_pixel_x_mags)
                self.y_magnitude_array.append(cur_pixel_y_mags)
                self.magnitude_array.append(cur_pixel_mags)
                self.angle_array.append(cur_pixel_angles)
                self.frames.append(cur_pixel_frames)
                self.temperatures_array.append(cur_pixel_temps)
                self.plotted_pixels.append(pixel)
        """
        for frame_index in range(self.frame_count):
            printProgressBar(frame_index, self.frame_count)
            if self.gui_instance is not None:
                self.gui_instance.update_progress_bar(frame_index,
                                                      self.frame_count)
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
                angle_rad = (np.arctan2(x_dir, y_dir) - (math.pi / 2)
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
        """

        if self.gui_instance is not None:
            self.gui_instance.remove_progress_bar()

    def calculateBins(self):
        for i, _ in enumerate(self.plotted_pixels):
            if self.angle_array[i]:
                self.angle_deg_maximum.append(np.amax(self.angle_array[i]))
                self.angle_deg_minimum.append(np.amin(self.angle_array[i]))
            if self.magnitude_array[i]:
                self.mag_minimum.append(np.amin(self.magnitude_array[i]))
                self.mag_maximum.append(np.amax(self.magnitude_array[i]))
                self.binning1.append(
                    int((abs(self.mag_maximum[i] - self.mag_minimum[i])) / 5))
                self.binning2.append(int(self.binning1[i] / 1.5))

    def plot3DBubble(self):
        for i, pixel in enumerate(self.plotted_pixels):
            relativeLoc = self.relativeLoc
            print(relativeLoc)
            if relativeLoc:
                title = 'Pixel Temp and Gradient Magnitude and Angle for: (' + str(
                    pixel[1]) + ',' + str(pixel[0]) + ') Threshold: ' + str(
                        self.threshold) + ' ' + str(
                            self.relativeLoc[0][i]) + '% From Right, ' + str(
                                self.relativeLoc[1][i]) + '% From Bottom'
            else:
                title = 'Pixel Temp and Gradient Magnitude and Angle for: (' + str(
                    pixel[1]) + ',' + str(pixel[0]) + ') Threshold: ' + str(
                        self.threshold)

            fig = go.Figure(data=go.Scatter3d(
                x=np.asarray(self.frames[i]).flatten(),
                y=np.asarray(self.magnitude_array[i]).flatten(),
                z=np.asarray(self.angle_array[i]).flatten(),
                text=np.asarray(self.temperatures_array[i]).flatten(),
                mode="markers",
                marker=dict(color=np.asarray(
                    self.temperatures_array[i]).flatten(),
                            size=5,
                            colorbar_title='Temperature')))
            fig.update_layout(height=1000,
                              width=1000,
                              title=title,
                              scene=dict(
                                  xaxis=dict(title='X: Frame'),
                                  yaxis=dict(title='Y: Gradient Magnitude'),
                                  zaxis=dict(title='Z: Gradient Angle')))
            fig.show()

    def plotMagnitude(self):
        # Plotting
        # Magnitude plot

        fig = []
        ax = []

        for i, pixel in enumerate(self.plotted_pixels):
            fig.append(None)
            ax.append(None)
            fig[i], ax[i] = plt.subplots()

            fig[i].suptitle(
                'Pixel {} Magnitude Histogram:\n{} Bins, Threshold: {}'.format(
                    (pixel[1], pixel[0]), self.binning1[i], self.threshold))

            ax[i].set_xlabel('Magnitude (sqrt(x^2+y^2))')
            ax[i].set_ylabel('Frequency')
            ax[i].hist(self.magnitude_array[i],
                       bins=self.binning1[i],
                       range=(self.mag_minimum[i], self.mag_maximum[i]),
                       edgecolor='black')
            ax[i].grid(b=self.grid_lines, which='major', alpha=0.3)
        """
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
        """

    def plotAngle(self):

        fig = []
        ax = []

        for i, pixel in enumerate(self.plotted_pixels):
            fig.append(None)
            ax.append(None)
            fig[i], ax[i] = plt.subplots()

            fig[i].suptitle(
                'Pixel {} Angle Histogram:\n{} Bins, Threshold: {}\n'.format(
                    (pixel[1], pixel[0]), self.binning2[i], self.threshold))

            ax[i].set_xlabel('Angle (°)')
            ax[i].set_ylabel('Frequency')
            ax[i].hist(self.angle_array[i],
                       bins=self.binning2[i],
                       range=(self.angle_deg_minimum[i],
                              self.angle_deg_maximum[i]),
                       edgecolor='black')
            ax[i].grid(b=self.grid_lines, which='major', alpha=0.3)
        """
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
        """

    def plot2DHistogram(self):
        histgrid = []
        fig = []
        ax = []
        histplot = []

        for i, pixel in enumerate(self.plotted_pixels):
            histgrid.append(None)
            fig.append(None)
            ax.append(None)
            histplot.append(None)
            histgrid[i] = (self.binning1[i], self.binning2[i])
            fig[i], ax[i] = plt.subplots()
            fig[i].suptitle(
                'Pixel {} Magnitude vs Angle Histogram:\nThreshold: {}\n'.
                format((pixel[1], pixel[0]), self.threshold))
            ax[i].set_xlabel('Angle (°)')
            ax[i].set_ylabel('Magnitude (sqrt(x^2+y^2))')
            histplot[i] = ax[i].hist2d(self.angle_array[i],
                                       self.magnitude_array[i],
                                       bins=histgrid[i],
                                       cmap='gnuplot')
            ax[i].grid(b=self.grid_lines, which='major', alpha=0.3)
            plt.colorbar(histplot[i][3])
        """
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
        """

    def plotScatter(self):
        # Scatterplot - Magnitude vs Angle (degrees)
        fig = []
        ax = []

        for i, pixel in enumerate(self.plotted_pixels):
            fig.append(None)
            ax.append(None)
            fig[i], ax[i] = plt.subplots()
            fig[i].suptitle(
                'Pixel {} Magnitude vs Angle Scatterplot:\nThreshold: {}\n'.
                format((pixel[1], pixel[0]), self.threshold))
            ax[i].set_xlabel('Angle (°)')
            ax[i].set_ylabel('Magnitude (sqrt(x^2+y^2))')
            ax[i].scatter(self.angle_array[i], self.magnitude_array[i])
            ax[i].grid(b=self.grid_lines, which='major', alpha=0.3)
        """
        fig4, ax4 = plt.subplots()
        fig4.suptitle(
            'Pixel {} Magnitude vs Angle Scatterplot:\nThreshold: {}\n'.format(
                self.cartesianPixel, self.threshold))
        ax4.set_xlabel('Angle (°)')
        ax4.set_ylabel('Magnitude (sqrt(x^2+y^2))')
        ax4.scatter(self.angle_array, self.magnitude_array)
        ax4.grid(b=self.grid_lines, which='major', alpha=0.3)
        """

    def plotHexBin(self):
        # "Hexbin plot" - Magnitude vs Angle (degrees)

        fig = []
        ax = []
        hexgrid = []
        hexplot = []

        for i, pixel in enumerate(self.plotted_pixels):
            fig.append(None)
            ax.append(None)
            hexgrid.append(None)
            hexplot.append(None)
            hexgrid[i] = (self.binning1[i], self.binning2[i])
            fig[i], ax[i] = plt.subplots()
            fig[i].suptitle(
                'Pixel {} Magnitude and Angle Hist:\nThreshold: {}\n'.format(
                    (pixel[1], pixel[0]), self.threshold))
            ax[i].set_xlabel('Angle (°)')
            ax[i].set_ylabel('Magnitude (sqrt(x^2+y^2))')
            hexplot[i] = ax[i].hexbin(self.angle_array[i],
                                      self.magnitude_array[i],
                                      gridsize=hexgrid[i],
                                      cmap='gnuplot')
            ax[i].grid(b=self.grid_lines, which='major', alpha=0.3)
            plt.colorbar(hexplot[i])
        """
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
        """

    def plotLine(self):

        pixelTempHistory = []
        frame = []

        for pixel in self.pixels:
            cur_pix_history = []
            cur_pix_frames = []
            for i, frame_data in enumerate(self.temp_data):
                printProgressBar(i + self.temp_data.start_frame,
                                 self.temp_data.end_frame,
                                 'Generating temp history plot.')
                cur_pix_frames.append(i + self.temp_data.start_frame)
                cur_pix_history.append(frame_data[pixel])
            pixelTempHistory.append(cur_pix_history)
            frame.append(cur_pix_frames)

        fig6, ax6 = plt.subplots()
        fig6.suptitle('Pixel {} Temperature History:\n'.format(self.pixels))
        ax6.set_xlabel('Frame')
        ax6.set_ylabel('Temperature')
        for history, frames, pixel in zip(pixelTempHistory, frame,
                                          self.pixels):
            ax6.plot(frames,
                     history,
                     label=str(pixel[1]) + ',' + str(pixel[0]))

        plt.legend()


if __name__ == '__main__':
    dataset = DataSet(
        '/home/troy/thermography/4-20_corrected/thermal_cam_temps.npy',
        end_frame=27000)
    plotter = Plots(dataset, [(50, 100), (123, 99)], threshold=500)
    plotter.plot3DBubble()
    plt.show()
