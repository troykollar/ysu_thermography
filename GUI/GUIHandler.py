import graphing
from tkinter import *
from tkinter import filedialog
from viewer import Viewer, colormap_frame
from dataset import DataSet
from composite import *
from plot import Plots
from matplotlib import pyplot as plt
from pixel_selector import PixelSelector


def browseFiles(self, entry):
    entry.delete(0, END)
    self.root.filepath = filedialog.askdirectory(initialdir="~/Documents")
    entry.insert(0, self.root.filepath)


def createPlotTool(self):
    return Plots(temp_data=self.tempData.get(),
                 pixel=(int(self.plot_PixelLocX.get()),
                        int(self.plot_PixelLocY.get())),
                 threshold=int(self.plot_TempThresh.get()),
                 start_frame=int(self.plot_StartFrame.get()),
                 end_frame=int(self.plot_EndFrame.get()),
                 gui_instance=self)


def play(self):
    grab_dataset(self)
    grab_viewer(self)
    self.viewer.play_video(self.frame_delay.get())


def save(self):
    grab_dataset(self)
    grab_viewer(self)
    self.viewer.save_video(framerate=self.framerate.get())


def grab_dataset(self):
    self.dataset = DataSet(self.tempData.get() + '/thermal_cam_temps.npy',
                           self.tempData.get() +
                           '/merged_data.npy' if self.info_pane else None,
                           remove_top_reflection=self.remove_top.get(),
                           remove_bottom_reflection=self.remove_bot.get(),
                           scale_factor=self.scale_factor.get(),
                           start_frame=self.start_frame.get(),
                           end_frame=self.end_frame.get())


def grab_viewer(self):
    self.viewer = Viewer(self.dataset, self.contour_threshold.get(),
                         self.follow.get(), self.follow_size.get(),
                         self.info_pane.get())


def save_thresh_img(self):
    grab_dataset(self)
    ThresholdImg(self.dataset, self.composite_threshold.get(), self).save_img()


def save_integration_img(self):
    grab_dataset(self)
    IntegrationImg(self.dataset, self.composite_threshold.get(),
                   self).save_img()


def save_avg_composite(self):
    grab_dataset(self)
    AvgImg(self.dataset, self).save_img()


def save_max_composite(self):
    grab_dataset(self)
    MaxImg(self.dataset, self).save_img()


def save_hotspot_composite(self):
    grab_dataset(self)
    HotspotImg(self.dataset, self).save_img()


def create_plots(self, pixel: tuple, relativeLoc=(0, 0)):
    grab_dataset(self)
    PLOTS = Plots(temp_data=self.dataset,
                  pixel=pixel,
                  threshold=int(self.plot_TempThresh.get()),
                  start_frame=int(self.plot_StartFrame.get()),
                  end_frame=int(self.plot_EndFrame.get()),
                  relativeLoc=relativeLoc)

    if self.grad_all.get():
        PLOTS.all()

    elif self.grad_mag.get():
        PLOTS.plotMagnitude()

    elif self.grad_angle.get():
        PLOTS.plotAngle()

    elif self.grad_2dHist.get():
        PLOTS.plot2DHistogram()

    elif self.grad_scatter.get():
        PLOTS.plotScatter()

    elif self.grad_hexBin.get():
        PLOTS.plotHexBin()

    elif self.grad_3D.get():
        PLOTS.plot3DBubble()

    elif self.plot_line.get():
        PLOTS.plotLine()

    plt.show()


def select_pixels(self):
    grab_dataset(self)
    thresh_img = ThresholdImg(self.dataset,
                              threshold=int(self.plot_TempThresh.get()),
                              gui_instance=self).img
    thresh_img = colormap_frame(thresh_img)
    pix_sel = PixelSelector()
    pix_sel.create_window('Select pixels for analysis', thresh_img)

    locations = pix_sel.location_list[2:]
    right_percents = pix_sel.percents_from_right[2:]
    bot_percents = pix_sel.percents_from_bot[2:]
    for pixel, right, bot in zip(locations, right_percents, bot_percents):
        create_plots(self, pixel, (right * 100, bot * 100))
