import graphing
from tkinter import *
from tkinter import filedialog

from np_vid_viewer.np_vid_viewer import NpVidTool
from plot import Plots


def submit(self):

    if self.gen_threshold_img.get():
        self.generate_threshold_image(self.tempDataEntry.get() + "/thermal_cam_temps.npy",
                                      int(self.genthreshold_thresholdInput.get()))

    if self.play_video.get():
        VIEWER = createNpVidTool(self)

        VIEWER.play_video(scale_factor=int(self.scaleFactor.get()),
                          frame_delay=int(self.frameDelay.get()))

    if self.save_video.get():
        VIEWER = createNpVidTool(self)

        VIEWER.save_video(scale_factor=int(self.scaleFactor.get()),
                          framerate=int(self.frameRate.get()), start=int(self.saveStartFrame.get()),
                          end=self.saveEndFrame.get())

    if self.save_frame.get():
        VIEWER = createNpVidTool(self)
        VIEWER.save_frame16(int(self.saveFrameNumber.get()), self.saveImageNumber.get())

    if self.pixel_temp_range.get():
        graphing.plotLine(temp_file=self.tempData.get() + "/thermal_cam_temps.npy",
                          pixel=(int(self.plotPixelLocX.get()), int(self.plotPixelLocY.get())),
                          startFrame=int(self.plotStartFrame.get()),
                          endFrame=int(self.plotEndFrame.get()))

    if self.gradient_plots.get():
        PLOTS = createPlotTool(self)



def browseFiles(self, entry):
    entry.delete(0, END)
    self.root.filepath = filedialog.askdirectory(initialdir="/home/rjyarwood/Documents/Research/ResearchData")
    entry.insert(0, self.root.filepath)


def createNpVidTool(self):
    return NpVidTool(data_directory=self.tempData.get(),
                     r_top_refl=int(self.removeTopReflection.get()),
                     r_bot_refl=int(self.removeBottomReflection.get()),
                     mp_data_on_vid=int(self.displayMeltPool.get()),
                     follow_max_temp=int(self.pixelAroundMax.get()),
                     contour_threshold=int(self.contourTempThresh.get()),
                     follow_contour=int(self.contourPixelRange.get()),
                     contour_data_on_img=int(self.displayContour.get()))


def createPlotTool(self):
    return Plots(temp_data=self.tempData.get(),
                 pixel=(int(self.plot_PixelLocX.get()), int(self.plot_PixelLocY.get())),
                 threshold=int(self.plot_TempThresh.get()),
                 start_frame=int(self.plot_StartFrame.get()),
                 end_frame=int(self.plot_EndFrame.get()))

