

import graphing
from tkinter import *
from tkinter import filedialog
import numpy as np

from GUI.select_pixels import selectPixels
from np_vid_viewer.np_vid_viewer import NpVidTool
from plot import Plots


def submit(self):

    if self.gen_threshold_img.get():
        self.generate_threshold_image(self.tempDataEntry.get() + "/thermal_cam_temps.npy",
                                      int(self.genthreshold_thresholdInput.get()))

    if self.play_video.get():
        VIEWER = createNpVidTool(self)

        VIEWER.play_video(scale_factor=int(self.play_scaleFactor.get()),
                          frame_delay=int(self.play_frameDelay.get()))

    if self.save_video.get():
        VIEWER = createNpVidTool(self)

        VIEWER.save_video(scale_factor=int(self.play_scaleFactor.get()),
                          framerate=int(self.play_frameRate.get()), start=int(self.play_saveStartFrame.get()),
                          end=self.play_saveEndFrame.get())

    if self.save_frame.get():
        VIEWER = createNpVidTool(self)
        VIEWER.save_frame16(int(self.saveFrameNumber.get()), self.saveImageNumber.get())

    if self.pixel_temp_range.get():
        graphing.plotLine(temp_file=self.tempData.get() + "/thermal_cam_temps.npy",
                          pixel=(int(self.plot_PixelLocX.get()), int(self.plot_PixelLocY.get())),
                          startFrame=int(self.plot_StartFrame.get()),
                          endFrame=int(self.plot_EndFrame.get()))

    if self.gradient_plots.get():

        if self.select_pixels.get():
            selectPixels(self=self,
                         temp_file=self.tempData.get() + "/thermal_cam_temps.npy",
                         composite_threshold=int(self.plot_TempThresh.get()),
                         start_frame=int(self.plot_StartFrame.get()),
                         end_frame=int(self.plot_EndFrame.get()))
        else:
            PLOTS = createPlotTool(self)

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

            elif self.grad_3d.get():
                PLOTS.plot3DBubble()


def browseFiles(self, entry):
    entry.delete(0, END)
    self.root.filepath = filedialog.askdirectory(initialdir="/home/rjyarwood/Documents/Research/ResearchData")
    entry.insert(0, self.root.filepath)


def createNpVidTool(self):
    return NpVidTool(data_directory=self.tempData.get(),
                     r_top_refl=int(self.play_removeTopReflection.get()),
                     r_bot_refl=int(self.play_removeBottomReflection.get()),
                     mp_data_on_vid=int(self.play_displayMeltPool.get()),
                     follow_max_temp=int(self.play_pixelAroundMax.get()),
                     contour_threshold=int(self.play_contourTempThresh.get()),
                     follow_contour=int(self.play_contourPixelRange.get()),
                     contour_data_on_img=int(self.play_displayContour.get()))


def createPlotTool(self):
    return Plots(temp_data=np.load(self.tempData.get() + "/thermal_cam_temps.npy", allow_pickle=True, mmap_mode='r'),
                 pixel=(int(self.plot_PixelLocX.get()), int(self.plot_PixelLocY.get())),
                 threshold=int(self.plot_TempThresh.get()),
                 start_frame=int(self.plot_StartFrame.get()),
                 end_frame=int(self.plot_EndFrame.get()))
