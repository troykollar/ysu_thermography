from np_vid_viewer import *
import graphing


def submit(self):

    if self.genThresholdImg.get():
        self.generate_threshold_image(self.tempDataEntry.get() + "/thermal_cam_temps.npy", int(self.genthreshold_thresholdInput.get()))

    if self.playVideo.get():
        VIEWER = NpVidTool(data_directory=self.tempDataEntry.get(),
                           r_top_refl=int(self.play_top_ref.get()),
                           r_bot_refl=int(self.play_bot_ref.get()),
                           mp_data_on_vid=int(self.play_disp_mp.get()),
                           follow_max_temp=int(self.play_fmaxInput.get()),
                           contour_threshold=int(self.play_cthreshInput.get()),
                           follow_contour=int(self.play_fcontourInput.get()),
                           contour_data_on_img=int(False))

        VIEWER.play_video(scale_factor=int(self.play_scaleFactorInput.get()),
                          frame_delay=int(self.play_frameDelayInput.get()))

    if self.saveVideo.get():
        VIEWER = NpVidTool(data_directory=self.tempDataEntry.get(),
                           r_top_refl=int(self.play_top_ref.get()),
                           r_bot_refl=int(self.play_bot_ref.get()),
                           mp_data_on_vid=int(self.play_disp_mp.get()),
                           follow_max_temp=int(self.play_fmaxInput.get()),
                           contour_threshold=int(self.play_cthreshInput.get()),
                           follow_contour=int(self.play_fcontourInput.get()))

        # TODO: Add start and end frame options
        VIEWER.save_video(scale_factor=int(self.play_scaleFactorInput.get()),
                          framerate=int(self.save_fpsInput.get()))

    if self.saveFrame.get():
        VIEWER = NpVidTool(data_directory=self.tempDataEntry.get())
        VIEWER.save_frame16(int(self.frameInput.get()), self.destDataEntry.get())

    if self.gradientHistogram.get():
        self.graphing.plotHistogram(temp_file=self.tempDataEntry.get() + "/thermal_cam_temps.npy",
                                    pixel=(int(self.pixelXLocationInput.get()), int(self.pixelYLocationInput.get())),
                                    threshold=int(self.histthreshInput.get()),
                                    binCount=int(self.histBinInput.get()),
                                    spacing=int(self.histGradSpacingInput.get()))

    if self.pixelTempRange.get():
        graphing.plotLine(temp_file=self.tempDataEntry.get() + "/thermal_cam_temps.npy",
                          pixel=(int(self.pixelXLocationInput.get()), int(self.pixelYLocationInput.get())),
                          startFrame=int(self.plotStartFrameInput.get()),
                          endFrame=int(self.plotEndFrameInput.get()))


def browseFiles(self, entry):
    entry.delete(0, self.END)
    self.root.filepath = self.filedialog.askdirectory(initialdir="/home/rjyarwood/Documents/Research/ResearchData")
    entry.insert(0, self.root.filepath)
