import numpy as np
import math
from matplotlib import pyplot as plt


class PlotGen:
    def __init__(self,
                 temp_data: np.ndarray,
                 pixel: tuple,
                 threshold: int,
                 start_frame=-1,
                 end_frame=-1):
        self.temp_data = temp_data
        self.pixel = pixel
        self.threshold = threshold
        self.start_frame, self.end_frame = self.validate_start_end_frames(
            start_frame, end_frame)

    def validate_start_end_frames(self, start_frame, end_frame):
        final_data_frame = self.temp_data.shape[0]
        if start_frame < 0:
            start_frame = 0
        elif start_frame > final_data_frame:
            start_frame = 0

        if end_frame < 0 or end_frame > final_data_frame:
            end_frame = final_data_frame

        return start_frame, end_frame

    def printProgressBar(self, iteration, total, prefix=''):
        suffix = ''
        length = 40
        fill = '█'
        print_end = "\r"
        decimals = 1
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
              end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print('\n')


class DataVisualizer(PlotGen):
    def __init__(self,
                 temp_data: np.ndarray,
                 pixel: tuple,
                 threshold: int,
                 start_frame=-1,
                 end_frame=-1):
        super().__init__(temp_data, pixel, threshold, start_frame, end_frame)
        self.directions = []
        self.angles_deg = []
        self.magnitudes = []
        self.pixel_temps = []

        # Turns true after running gather data, so it can be run automatically
        self.data_gathered = False

    def gather_data(self):
        for i, frame in enumerate(
                self.temp_data[self.start_frame:self.end_frame]):
            self.printProgressBar(i, self.end_frame, 'Gathering data...')
            pixel_x = self.pixel[0]
            pixel_y = self.pixel[1]
            cur_pixel_temp = frame[pixel_y, pixel_x]
            result_matrix = np.asmatrix(frame)

            if cur_pixel_temp > self.threshold:
                self.pixel_temps.append(cur_pixel_temp)

                dy, dx = np.gradient(
                    result_matrix)  # Retrieve image gradient data
                x_dir = dx[pixel_x, pixel_y]  # Pixel magnitude W.R.T. x-axis
                y_dir = dy[pixel_x, pixel_y]  # Pixel magnitude W.R.T. y-axis
                self.directions.append((x_dir, y_dir))

                # Calc magnitude and add to magnitude array
                magnitude = math.sqrt((x_dir**2) + (y_dir**2))
                self.magnitudes.append(magnitude)

                # Calc angle and add to angle array
                angle_rad = (np.arctan2(y_dir, x_dir) - (math.pi / 2)
                             )  #shift -90 deg
                angle_deg = (angle_rad * (180 / math.pi))  #Convert to degrees
                self.angles_deg.append(angle_deg)
        self.data_gathered = True

    def generate_plots(self, gridlines=True):
        if not self.data_gathered:
            self.gather_data()

        threshold = self.threshold
        mag_arr = self.magnitudes
        angle_arr_deg = self.angles_deg
        pixel_x = self.pixel[0]
        pixel_y = self.pixel[1]
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


if __name__ == '__main__':
    temp_data_fname = '/home/troy/thermography/4-20_corrected/thermal_cam_temps.npy'
    temp_data = np.load(temp_data_fname, allow_pickle=True, mmap_mode='r')
    dv = DataVisualizer(temp_data, (120, 110), 500)
    dv.generate_plots()