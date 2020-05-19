from tkinter import *
from GUI import Descriptors, ToolTip
from GUI import GUIHandler as handler
import GUI.constants as consts
from GUI import helper_functions as func
from viewer import Viewer, colormap_frame
from dataset import DataSet
from composite import get_threshold_img, save_threshold_img
from plot import Plots
from matplotlib import pyplot as plt
from pixel_selector import PixelSelector


class GUI:
    def __init__(self):
        self.ACTIVEBACKGROUND = consts.ACTIVEBACKGROUND
        self.ACTIVEBUTTONBACKGROUND = consts.ACTIVEBUTTONBACKGROUND
        self.ACTIVEFIELDBACKGROUND = consts.ACTIVEFIELDBACKGROUND
        self.ACTIVEFRAMEBORDER = consts.ACTIVEFRAMEBORDER
        self.TEXTCOLOR = consts.TEXTCOLOR

        self.INACTIVEBACKGROUND = consts.INACTIVEBACKGROUND
        self.INACTIVEBUTTONBACKGROUND = consts.INACTIVEBUTTONBACKGROUND
        self.INACTIVEFIELDBACKGROUND = consts.INACTIVEFIELDBACKGROUND
        self.INACTIVEFRAMEBORDER = consts.INACTIVEFRAMEBORDER

        self.root = Tk()
        self.root.title("YSU Thermography")
        self.root['bg'] = self.ACTIVEBACKGROUND
        # root.iconbitmap("images/YSU_Logo")

        # Creating variables for checkboxes to change
        self.dataset = None
        self.viewer = None

        # Dataset related variables
        self.remove_top = BooleanVar(False)
        self.remove_bot = BooleanVar(False)
        self.scale_factor = IntVar(value=1)
        self.start_frame = IntVar(value=-1)
        self.end_frame = IntVar(value=-1)

        # Viewer related variables
        self.contour_threshold = IntVar(value=None)
        self.follow = StringVar(value=None)
        self.follow_size = IntVar(value=20)
        self.info_pane = StringVar(value=None)
        self.frame_delay = IntVar(value=1)
        self.framerate = IntVar(value=60)

        # Composite related variables
        self.composite_threshold = IntVar(value=None)

        self.generate_img = BooleanVar(False)
        self.save_frame = BooleanVar()
        self.play_video = BooleanVar(False)
        self.save_video = BooleanVar(False)
        self.gen_threshold_img = BooleanVar(False)
        self.data_set = BooleanVar()
        self.gradient_plots = BooleanVar()
        self.pixel_temp_range = BooleanVar()

        self.tempData = StringVar()

        self.genthreshold_threshold = StringVar()

        self.save_FrameNumber = StringVar()
        self.save_ImageNumber = StringVar()

        self.play_scaleFactor = StringVar()
        self.play_frameDelay = StringVar()
        self.play_pixelAroundMax = StringVar()
        self.play_contourTempThresh = StringVar()
        self.play_contourPixelRange = StringVar()
        self.play_frameRate = StringVar()
        self.play_removeTopReflection = BooleanVar()
        self.play_removeBottomReflection = BooleanVar()
        self.play_displayMeltPool = BooleanVar()
        self.play_saveStartFrame = StringVar()
        self.play_saveEndFrame = StringVar()
        self.play_displayContour = BooleanVar()

        self.plot_PixelLocX = StringVar()
        self.plot_PixelLocY = StringVar()
        self.plot_TempThresh = StringVar()
        self.plot_StartFrame = StringVar()
        self.plot_EndFrame = StringVar()
        self.grad_mag = BooleanVar()
        self.grad_angle = BooleanVar()
        self.grad_2dHist = BooleanVar()
        self.grad_scatter = BooleanVar()
        self.grad_hexBin = BooleanVar()
        self.grad_3D = BooleanVar()
        self.grad_all = BooleanVar()

        # Creating Frame Sections
        self.filePanel = Frame(self.root, bg=self.ACTIVEBACKGROUND)
        self.filePanel.pack(side=TOP, fill=BOTH, pady=10)

        self.dataset_panel = Frame(self.root, bg=self.ACTIVEBACKGROUND)
        self.dataset_panel.pack(side=TOP, fill=BOTH, pady=10)

        self.viewer_panel = Frame(self.root, bg=self.ACTIVEBACKGROUND)
        self.viewer_panel.pack(side=TOP, fill=BOTH, pady=10)

        self.optionsPanel = Frame(self.root,
                                  bg=self.ACTIVEBACKGROUND,
                                  bd=1,
                                  highlightthickness=1,
                                  highlightcolor=self.ACTIVEFRAMEBORDER,
                                  highlightbackground=self.ACTIVEFRAMEBORDER,
                                  padx=5,
                                  relief=FLAT)
        self.optionsPanel.pack(fill=BOTH)

        self.optionsPanel.columnconfigure(0, weight=1)
        self.optionsPanel.columnconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(0, weight=1)
        self.optionsPanel.rowconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(2, weight=1)
        self.optionsPanel.rowconfigure(3, weight=1)

        # Building  all frames
        self.buildFileFrame()
        self.build_dataset_frame()
        self.build_viewer_frame()
        self.build_composite_frame()
        self.buildPlotOptionsFrame()

        # Main GUI loop
        self.root.mainloop()

    def gradSelectAll(self):
        if self.grad_all.get():
            self.grad_mag.set(1)
            self.grad_angle.set(1)
            self.grad_2dHist.set(1)
            self.grad_scatter.set(1)
            self.grad_hexBin.set(1)
            self.grad_3D.set(1)

    def buildFileFrame(self):
        tempDataLabel = Label(self.filePanel,
                              text="File Path Build Data Folder: ",
                              padx=0,
                              pady=0,
                              bg=self.ACTIVEBACKGROUND,
                              foreground=self.TEXTCOLOR)
        tempDataHint = Descriptors.getHintTextFileFrame('tempDataLabel')
        ToolTip.createToolTip(tempDataLabel, tempDataHint)
        tempDataLabel.pack(side=LEFT)
        tempDataEntry = Entry(self.filePanel,
                              width=75,
                              textvariable=self.tempData,
                              relief=FLAT,
                              bg=self.ACTIVEFIELDBACKGROUND,
                              foreground=self.TEXTCOLOR)
        tempDataEntry.pack(side=LEFT)

        tempDataBrowse = Button(
            self.filePanel,
            text="Browse",
            command=lambda: handler.browseFiles(self, tempDataEntry),
            bd=2,
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT,
            padx=0,
            pady=0,
            activeforeground=self.TEXTCOLOR,
            foreground=self.TEXTCOLOR)
        tempDataBrowse.pack(side=LEFT)

    def build_dataset_frame(self):
        # TODO: Update hints
        # Main Frame
        self.dataset_frame = func.buildOuterLabelFrame(obj=self,
                                                       root=self.dataset_panel,
                                                       label='Dataset Options')

        self.dataset_frame.grid(row=0,
                                column=0,
                                columnspan=2,
                                sticky=W + E + N + S,
                                ipady=5,
                                pady=5)

        self.dataset_frame.columnconfigure(0, weight=1)
        self.dataset_frame.columnconfigure(1, weight=1)
        self.dataset_frame.columnconfigure(2, weight=1)
        self.dataset_frame.columnconfigure(3, weight=1)
        self.dataset_frame.columnconfigure(4, weight=1)
        self.dataset_frame.rowconfigure(0, weight=1)

        # Frame to hold checkbox to remove top reflection
        remove_top_label = func.buildInnerLabelFrame(
            obj=self, root=self.dataset_frame, label='Remove Top Reflection')

        remove_top_hint = 'Remove top reflections from data'
        ToolTip.createToolTip(remove_top_label, remove_top_hint)

        remove_top_label.grid(row=0, column=0, sticky=W + E + N + S)

        remove_top_cb = func.buildFunctionCheckButton(obj=self,
                                                      root=remove_top_label,
                                                      variable=self.remove_top,
                                                      command=None)
        remove_top_cb.pack()

        # Frame to hold checkbox to remove bottom reflection
        remove_bot_label = func.buildInnerLabelFrame(
            obj=self,
            root=self.dataset_frame,
            label='Remove Bottom Reflection')

        remove_bot_hint = 'Remove top reflections from data'
        ToolTip.createToolTip(remove_bot_label, remove_bot_hint)

        remove_bot_label.grid(row=0, column=1, sticky=W + E + N + S)

        remove_bot_cb = func.buildFunctionCheckButton(obj=self,
                                                      root=remove_bot_label,
                                                      variable=self.remove_bot,
                                                      command=None)
        remove_bot_cb.pack()

        # Frame to hold entry for scale factor
        scale_factor_label = func.buildInnerLabelFrame(obj=self,
                                                       root=self.dataset_frame,
                                                       label='Scale Factor')

        scale_factor_hint = 'Factor used to scale data.'
        ToolTip.createToolTip(scale_factor_label, scale_factor_hint)

        scale_factor_label.grid(row=0, column=2, sticky=W + E + N + S)

        scale_factor_entry = func.buildEntry(obj=self,
                                             root=scale_factor_label,
                                             textvariable=self.scale_factor)
        scale_factor_entry.pack()

        # Frame to hold entry for scale factor
        start_frame_label = func.buildInnerLabelFrame(obj=self,
                                                      root=self.dataset_frame,
                                                      label='Start Frame')

        start_frame_hint = 'Factor used to scale data.'
        ToolTip.createToolTip(start_frame_label, start_frame_hint)

        start_frame_label.grid(row=0, column=3, sticky=W + E + N + S)

        start_frame_entry = func.buildEntry(obj=self,
                                            root=start_frame_label,
                                            textvariable=self.start_frame)
        start_frame_entry.pack()

        # Frame to hold entry for scale factor
        end_frame_label = func.buildInnerLabelFrame(obj=self,
                                                    root=self.dataset_frame,
                                                    label='End Frame')

        end_frame_hint = 'Factor used to scale data.'
        ToolTip.createToolTip(end_frame_label, end_frame_hint)

        end_frame_label.grid(row=0, column=4, sticky=W + E + N + S)

        end_frame_entry = func.buildEntry(obj=self,
                                          root=end_frame_label,
                                          textvariable=self.end_frame)
        end_frame_entry.pack()

    def build_viewer_frame(self):
        # Main Frame
        self.viewer_frame = func.buildOuterLabelFrame(obj=self,
                                                      root=self.viewer_panel,
                                                      label='Viewer Options')

        self.viewer_frame.grid(row=0,
                               column=0,
                               columnspan=2,
                               sticky=W + E + N + S,
                               ipady=5,
                               pady=5)

        self.viewer_frame.columnconfigure(0, weight=1)
        self.viewer_frame.columnconfigure(1, weight=1)
        self.viewer_frame.columnconfigure(2, weight=1)
        self.viewer_frame.columnconfigure(3, weight=1)
        self.viewer_frame.columnconfigure(4, weight=1)
        self.viewer_frame.rowconfigure(0, weight=1)

        # Frame to hold entry for contour threshold
        contour_thresh_label = func.buildInnerLabelFrame(
            obj=self, root=self.viewer_frame, label='Contour Threshold')

        contour_thresh_hint = 'Threshold used for contouring.'
        ToolTip.createToolTip(contour_thresh_label, contour_thresh_hint)

        contour_thresh_label.grid(row=0, column=0, sticky=W + E + N + S)

        contour_thresh_entry = func.buildEntry(
            obj=self,
            root=contour_thresh_label,
            textvariable=self.contour_threshold)
        contour_thresh_entry.pack()

        # Radio buttons to determine what to focus frame on
        follow_buttons_dict = {
            'Contour': 'contour',
            'Max Temp': 'max',
            'None': None
        }

        follow_buttons_frame = self.build_radio_button_set(
            self.viewer_frame, 'Frame focus', follow_buttons_dict, self.follow)
        follow_buttons_frame.grid(row=0, column=1, sticky=W + E + N + S)

        # Frame to hold entry for follow_size
        follow_size_frame = func.buildInnerLabelFrame(
            obj=self, root=self.viewer_frame, label='Focused frame size')

        follow_size_hint = 'How many pixels to be shown on either side of the focused pixel.'
        ToolTip.createToolTip(follow_size_frame, follow_size_hint)

        follow_size_frame.grid(row=0, column=2, sticky=W + E + N + S)

        follow_size_entry = func.buildEntry(obj=self,
                                            root=follow_size_frame,
                                            textvariable=self.follow_size)
        follow_size_entry.pack()

        # Radio buttons to determine what info pane to show
        info_buttons_dict = {
            'Contour': 'contour',
            'Meltpool': 'mp',
            'None': None
        }

        info_buttons_frame = self.build_radio_button_set(
            self.viewer_frame, 'Info Pane', info_buttons_dict, self.info_pane)
        info_buttons_frame.grid(row=0, column=3, sticky=W + E + N + S)

        execute_buttons_frame = func.buildInnerLabelFrame(
            obj=self, root=self.viewer_frame, label=None)
        execute_buttons_frame.columnconfigure(0, weight=1)
        execute_buttons_frame.columnconfigure(1, weight=1)
        execute_buttons_frame.rowconfigure(0, weight=1)
        execute_buttons_frame.rowconfigure(1, weight=1)
        execute_buttons_frame.rowconfigure(2, weight=1)
        execute_buttons_frame.grid(row=0, column=4, sticky=W + E + N + S)

        play_button = Button(execute_buttons_frame,
                             text='Play Video',
                             command=lambda: self.play(),
                             bg=self.ACTIVEBUTTONBACKGROUND,
                             relief=FLAT)
        play_button.grid(row=0, column=0)
        frame_delay_entry = func.buildEntry(obj=self,
                                            root=execute_buttons_frame,
                                            textvariable=self.frame_delay)
        frame_delay_entry.grid(row=0, column=1)

        save_video_button = Button(execute_buttons_frame,
                                   text='Save Video',
                                   command=lambda: self.save(),
                                   bg=self.ACTIVEBUTTONBACKGROUND,
                                   relief=FLAT)
        save_video_button.grid(row=1, column=0)
        framerate_entry = func.buildEntry(obj=self,
                                          root=execute_buttons_frame,
                                          textvariable=self.framerate)
        framerate_entry.grid(row=1, column=1)

        save_frame_button = Button(execute_buttons_frame,
                                   text='Save Frames',
                                   command=lambda: self.save_frames(),
                                   bg=self.ACTIVEBUTTONBACKGROUND,
                                   relief=FLAT)
        save_frame_button.grid(row=2, column=0)

    def build_composite_frame(self):
        self.composite_frame = func.buildOuterLabelFrame(
            obj=self, root=self.optionsPanel, label='Composite options')

        self.composite_frame.grid(row=1,
                                  column=0,
                                  sticky=W + E + N + S,
                                  ipady=5,
                                  pady=5,
                                  padx=5)

        threshold_frame = func.buildInnerLabelFrame(
            obj=self, root=self.composite_frame, label='Temperature Threshold')

        threshold_hint = 'Threshold used to increment image.'
        ToolTip.createToolTip(threshold_frame, threshold_hint)
        threshold_frame.pack(side=LEFT, expand=1)

        threshold_input = func.buildEntry(
            obj=self,
            root=threshold_frame,
            textvariable=self.composite_threshold)
        threshold_input.pack()

        gen_threshold_button = Button(
            self.composite_frame,
            text='Generate Threshold Image',
            command=lambda: self.save_threshold_img(),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        gen_threshold_button.pack()

    def buildPlotOptionsFrame(self):
        self.plotOptionsFrame = func.buildOuterLabelFrame(
            obj=self, root=self.optionsPanel, label='Plot Options')

        self.plotOptionsFrame.grid(row=3,
                                   column=0,
                                   columnspan=2,
                                   sticky=W + E + N + S)

        self.plotOptionsFrame.columnconfigure(0, weight=1)
        self.plotOptionsFrame.columnconfigure(1, weight=1)
        self.plotOptionsFrame.columnconfigure(2, weight=1)
        self.plotOptionsFrame.rowconfigure(0, weight=1)
        self.plotOptionsFrame.rowconfigure(1, weight=1)
        self.plotOptionsFrame.rowconfigure(2, weight=1)

        pixelLocationFrame = func.buildInnerLabelFrame(
            obj=self, root=self.plotOptionsFrame, label='Pixel Location')

        pixelLocationHint = Descriptors.getHintTextPlotOptions(
            'pixelLocationFrame')
        ToolTip.createToolTip(pixelLocationFrame, pixelLocationHint)
        pixelLocationFrame.grid(row=0, column=1, sticky=W + E + N + S)

        pixelLocationFrame.columnconfigure(0, weight=1)
        pixelLocationFrame.columnconfigure(1, weight=1)
        pixelLocationFrame.columnconfigure(2, weight=1)
        pixelLocationFrame.columnconfigure(3, weight=1)
        pixelLocationFrame.rowconfigure(0, weight=1)

        pixelXLocationInput = func.buildEntry(obj=self,
                                              root=pixelLocationFrame,
                                              textvariable=self.plot_PixelLocX)

        pixelXLocationInput.grid(row=0, column=0, sticky=W + E + N + S)
        comma = Label(pixelLocationFrame,
                      text=",",
                      bd=0,
                      highlightthickness=0,
                      bg=self.ACTIVEBACKGROUND)
        comma.grid(row=0, column=1, sticky=W + E + N + S)
        pixelYLocationInput = func.buildEntry(obj=self,
                                              root=pixelLocationFrame,
                                              textvariable=self.plot_PixelLocY)

        pixelYLocationInput.grid(row=0, column=2, sticky=W + E + N + S)

        select_pixels_button = Button(pixelLocationFrame,
                                      text='Select Pixels',
                                      command=lambda: self.select_pixels(),
                                      bg=self.ACTIVEBUTTONBACKGROUND,
                                      relief=FLAT)

        select_pixels_button.grid(row=0, column=3)

        histthreshFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.plotOptionsFrame,
                                                    label='Temp Thresh')

        histthreshHint = Descriptors.getHintTextPlotOptions('histthreshFrame')
        ToolTip.createToolTip(histthreshFrame, histthreshHint)
        histthreshFrame.grid(row=0, column=0, sticky=W + E + N + S)

        histthreshInput = func.buildEntry(obj=self,
                                          root=histthreshFrame,
                                          textvariable=self.plot_TempThresh)
        histthreshInput.insert(END, 200)
        histthreshInput.pack()

        frameRangeFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.plotOptionsFrame,
                                                    label='Frame Range')

        frameRangeHint = Descriptors.getHintTextPlotOptions('frameRangeFrame')
        ToolTip.createToolTip(frameRangeFrame, frameRangeHint)
        frameRangeFrame.grid(row=0, column=2, sticky=W + E + N + S)

        frameRangeFrame.columnconfigure(0, weight=1)
        frameRangeFrame.columnconfigure(1, weight=1)
        frameRangeFrame.rowconfigure(0, weight=1)

        plotStartFrameInput = func.buildEntry(
            obj=self, root=frameRangeFrame, textvariable=self.plot_StartFrame)
        plotStartFrameInput.insert(END, 0)
        plotStartFrameInput.grid(row=0, column=0)

        plotEndFrameInput = func.buildEntry(obj=self,
                                            root=frameRangeFrame,
                                            textvariable=self.plot_EndFrame)
        plotEndFrameInput.insert(END, -1)
        plotEndFrameInput.grid(row=0, column=1)

        self.gradFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=self.plotOptionsFrame,
                                                   label='Gradient Plots')

        self.gradFrame.grid(row=3, column=0, columnspan=3)

        gradMagFrame = func.buildInnerLabelFrame(
            obj=self, root=self.gradFrame, label='Gradient Magnitude Plot')
        gradMagFrame.grid(row=0, column=0)

        gradMagCheckButton = func.buildFlagCheckButton(obj=self,
                                                       root=gradMagFrame,
                                                       variable=self.grad_mag)
        gradMagCheckButton.pack()

        gradAngleFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=self.gradFrame,
                                                   label='Gradient Angle Plot')
        gradAngleFrame.grid(row=0, column=1)

        gradAngleCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradAngleFrame, variable=self.grad_angle)
        gradAngleCheckButton.pack()

        grad2dHistFrame = func.buildInnerLabelFrame(
            obj=self, root=self.gradFrame, label='Gradient 2D Histogram')
        grad2dHistFrame.grid(row=0, column=2)

        grad2dHistCheckButton = func.buildFlagCheckButton(
            obj=self, root=grad2dHistFrame, variable=self.grad_2dHist)
        grad2dHistCheckButton.pack()

        gradScatterFrame = func.buildInnerLabelFrame(
            obj=self, root=self.gradFrame, label='Gradient Scatter Plot')
        gradScatterFrame.grid(row=1, column=0)

        gradScatterCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradScatterFrame, variable=self.grad_scatter)
        gradScatterCheckButton.pack()

        gradHexBinFrame = func.buildInnerLabelFrame(
            obj=self, root=self.gradFrame, label='Gradient Hex Bin Plot')
        gradHexBinFrame.grid(row=1, column=1)

        gradHexBinCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradHexBinFrame, variable=self.grad_hexBin)
        gradHexBinCheckButton.pack()

        grad3dFrame = func.buildInnerLabelFrame(obj=self,
                                                root=self.gradFrame,
                                                label='3D Plot')
        grad3dFrame.grid(row=1, column=2)

        grad3dCheckButton = func.buildFlagCheckButton(obj=self,
                                                      root=grad3dFrame,
                                                      variable=self.grad_3D)
        grad3dCheckButton.pack()

        gradAllFrame = func.buildInnerLabelFrame(obj=self,
                                                 root=self.gradFrame,
                                                 label='All Plots')
        gradAllFrame.grid(row=2, column=1)

        gradAllCheckButton = func.buildFunctionCheckButton(
            obj=self,
            root=gradAllFrame,
            variable=self.grad_all,
            command=self.gradSelectAll)
        gradAllCheckButton.pack()

        create_plots_button = Button(self.plotOptionsFrame,
                                     text='Create Plots',
                                     command=lambda: self.create_plots(
                                         (int(self.plot_PixelLocX.get()),
                                          int(self.plot_PixelLocY.get()))),
                                     bg=self.ACTIVEBUTTONBACKGROUND,
                                     relief=FLAT)

        create_plots_button.grid(row=4, column=2)

    def build_radio_button_set(self, root, label: str, buttons: dict,
                               variable):
        radio_frame = func.buildInnerLabelFrame(obj=self,
                                                root=root,
                                                label=label)
        for key in buttons:
            Radiobutton(radio_frame,
                        text=key,
                        variable=variable,
                        value=buttons[key]).pack()

        return radio_frame

    def play(self):
        self.grab_dataset()
        self.grab_viewer()
        self.viewer.play_video(self.frame_delay.get())

    def save(self):
        self.grab_dataset()
        self.grab_viewer()
        self.viewer.save_video(framerate=self.framerate.get())

    def grab_dataset(self):
        self.dataset = DataSet(self.tempData.get() + '/thermal_cam_temps.npy',
                               self.remove_top.get(), self.remove_bot.get(),
                               self.scale_factor.get())

    def grab_viewer(self):
        self.viewer = Viewer(self.dataset, self.contour_threshold.get(),
                             self.follow.get(), self.follow_size.get(),
                             self.info_pane.get())

    def save_threshold_img(self):
        self.grab_dataset()
        thresh_img = get_threshold_img(self.dataset,
                                       self.composite_threshold.get(),
                                       self.start_frame.get(),
                                       self.end_frame.get())
        save_threshold_img(self.tempData.get(), thresh_img,
                           self.composite_threshold.get())

    def create_plots(self, pixel: tuple):
        self.grab_dataset()
        PLOTS = Plots(temp_data=self.dataset,
                      pixel=pixel,
                      threshold=int(self.plot_TempThresh.get()),
                      start_frame=int(self.plot_StartFrame.get()),
                      end_frame=int(self.plot_EndFrame.get()))

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

        plt.show()

    def select_pixels(self):
        self.grab_dataset()
        thresh_img = get_threshold_img(dataset=self.dataset,
                                       threshold=int(
                                           self.plot_TempThresh.get()),
                                       start=int(self.plot_StartFrame.get()),
                                       end=int(self.plot_EndFrame.get()))
        thresh_img = colormap_frame(thresh_img)
        pix_sel = PixelSelector()
        pix_sel.create_window('Select pixels for analysis', thresh_img)

        locations = pix_sel.location_list[2:]
        for pixel in locations:
            self.create_plots(pixel)
