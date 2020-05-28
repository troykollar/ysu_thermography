from tkinter import *
from GUI import Descriptors, ToolTip
from GUI import GUIHandler as handler
import GUI.constants as consts
import GUI.helper_functions as func
from helper_functions import get_description_dict

#TODO: Add meltpool data entry


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

        # Get description dictionary
        self.descriptions = get_description_dict()

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
        self.buildGradOptionsFrame()

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
        ToolTip.createToolTip(tempDataLabel, self.descriptions['temp_data'])
        tempDataLabel.pack(side=LEFT, fill=BOTH)
        tempDataEntry = Entry(self.filePanel,
                              width=75,
                              textvariable=self.tempData,
                              relief=FLAT,
                              bg=self.ACTIVEFIELDBACKGROUND,
                              foreground=self.TEXTCOLOR)
        tempDataEntry.pack(side=LEFT, fill=BOTH)

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
        # Main Frame
        self.dataset_frame = func.buildOuterLabelFrame(obj=self,
                                                       root=self.dataset_panel,
                                                       label='Dataset Options')

        self.dataset_frame.pack(fill=BOTH)

        self.dataset_frame.columnconfigure(0, weight=1)
        self.dataset_frame.columnconfigure(1, weight=1)
        self.dataset_frame.columnconfigure(2, weight=1)
        self.dataset_frame.columnconfigure(3, weight=1)
        self.dataset_frame.columnconfigure(4, weight=1)
        self.dataset_frame.rowconfigure(0, weight=1)

        # Frame to hold checkbox to remove top reflection
        remove_top_label = func.buildInnerLabelFrame(
            obj=self, root=self.dataset_frame, label='Remove Top Reflection')

        ToolTip.createToolTip(remove_top_label,
                              self.descriptions['remove_top'])

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

        ToolTip.createToolTip(remove_bot_label,
                              self.descriptions['remove_bot'])

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

        ToolTip.createToolTip(scale_factor_label,
                              self.descriptions['scale_factor'])

        scale_factor_label.grid(row=0, column=2, sticky=W + E + N + S)

        scale_factor_entry = func.buildEntry(obj=self,
                                             root=scale_factor_label,
                                             textvariable=self.scale_factor)
        scale_factor_entry.pack()

        # Frame to hold entry for start frame
        start_frame_label = func.buildInnerLabelFrame(obj=self,
                                                      root=self.dataset_frame,
                                                      label='Start Frame')

        ToolTip.createToolTip(start_frame_label,
                              self.descriptions['start_frame'])

        start_frame_label.grid(row=0, column=3, sticky=W + E + N + S)

        start_frame_entry = func.buildEntry(obj=self,
                                            root=start_frame_label,
                                            textvariable=self.start_frame)
        start_frame_entry.pack()

        # Frame to hold entry for end frame
        end_frame_label = func.buildInnerLabelFrame(obj=self,
                                                    root=self.dataset_frame,
                                                    label='End Frame')

        ToolTip.createToolTip(end_frame_label, self.descriptions['end_frame'])

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

        self.viewer_frame.pack(fill=BOTH)

        self.viewer_frame.columnconfigure(0, weight=1)
        self.viewer_frame.columnconfigure(1, weight=1)
        self.viewer_frame.columnconfigure(2, weight=1)
        self.viewer_frame.columnconfigure(3, weight=1)
        self.viewer_frame.columnconfigure(4, weight=1)
        self.viewer_frame.rowconfigure(0, weight=1)

        # Frame to hold entry for contour threshold
        contour_thresh_label = func.buildInnerLabelFrame(
            obj=self, root=self.viewer_frame, label='Contour Threshold')

        ToolTip.createToolTip(contour_thresh_label,
                              self.descriptions['contour_threshold'])

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

        ToolTip.createToolTip(follow_size_frame,
                              self.descriptions['follow_size'])

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
                             command=lambda: handler.play(self),
                             bg=self.ACTIVEBUTTONBACKGROUND,
                             relief=FLAT)
        play_button.grid(row=0, column=0)
        frame_delay_entry = func.buildEntry(obj=self,
                                            root=execute_buttons_frame,
                                            textvariable=self.frame_delay)
        frame_delay_entry.grid(row=0, column=1)

        save_video_button = Button(execute_buttons_frame,
                                   text='Save Video',
                                   command=lambda: handler.save(self),
                                   bg=self.ACTIVEBUTTONBACKGROUND,
                                   relief=FLAT)
        save_video_button.grid(row=1, column=0)
        framerate_entry = func.buildEntry(obj=self,
                                          root=execute_buttons_frame,
                                          textvariable=self.framerate)
        framerate_entry.grid(row=1, column=1)

        save_frame_button = Button(execute_buttons_frame,
                                   text='Save Frames',
                                   command=lambda: handler.save_frames(self),
                                   bg=self.ACTIVEBUTTONBACKGROUND,
                                   relief=FLAT)
        save_frame_button.grid(row=2, column=0)

    def build_composite_frame(self):
        self.composite_frame = func.buildOuterLabelFrame(
            obj=self, root=self.optionsPanel, label='Composite options')

        self.composite_frame.pack(fill=BOTH)

        threshold_frame = func.buildInnerLabelFrame(
            obj=self, root=self.composite_frame, label='Temperature Threshold')

        ToolTip.createToolTip(threshold_frame, self.descriptions['threshold'])
        threshold_frame.pack(side=LEFT, padx=10)

        threshold_input = func.buildEntry(
            obj=self,
            root=threshold_frame,
            textvariable=self.composite_threshold)
        threshold_input.pack()

        normal_composite_button = Button(
            self.composite_frame,
            text='Create Composite Image',
            command=lambda: handler.save_thresh_img(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        normal_composite_button.pack(side=LEFT, padx=40)

        integration_composite_button = Button(
            self.composite_frame,
            text='Integration Composite',
            command=lambda: handler.save_thresh_img(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        integration_composite_button.pack(side=LEFT, padx=40)

        other_composite_frame = func.buildInnerLabelFrame(obj=self, root=self.composite_frame,
                                                          label='Other Composite Images')
        other_composite_frame.pack(side=RIGHT, padx=40)

        average_composite_button = Button(
            other_composite_frame,
            text='Average Composite',
            command=lambda: handler.save_thresh_img(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        average_composite_button.pack()

        max_temp_composite_button = Button(
            other_composite_frame,
            text='Max Temp Composite',
            command=lambda: handler.save_thresh_img(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        max_temp_composite_button.pack()

        hotspot_composite_button = Button(
            other_composite_frame,
            text='Hot Spot Composite',
            command=lambda: handler.save_thresh_img(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)
        hotspot_composite_button.pack()


    def buildPlotOptionsFrame(self):
        self.plotOptionsFrame = func.buildOuterLabelFrame(
            obj=self, root=self.optionsPanel, label='Plot Options')

        self.plotOptionsFrame.pack(fill=BOTH)

        self.plotOptionsFrame.columnconfigure(0, weight=1)
        self.plotOptionsFrame.columnconfigure(1, weight=1)
        self.plotOptionsFrame.columnconfigure(2, weight=1)
        self.plotOptionsFrame.rowconfigure(0, weight=1)
        self.plotOptionsFrame.rowconfigure(1, weight=1)
        self.plotOptionsFrame.rowconfigure(2, weight=1)

        pixelLocationFrame = func.buildInnerLabelFrame(
            obj=self, root=self.plotOptionsFrame, label='Pixel Location')

        ToolTip.createToolTip(pixelLocationFrame,
                              self.descriptions['plot_pixel_location'])
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

        select_pixels_button = Button(
            pixelLocationFrame,
            text='Select Pixels',
            command=lambda: handler.select_pixels(self),
            bg=self.ACTIVEBUTTONBACKGROUND,
            relief=FLAT)

        select_pixels_button.grid(row=0, column=3)

        histthreshFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.plotOptionsFrame,
                                                    label='Temp Thresh')

        ToolTip.createToolTip(histthreshFrame, self.descriptions['threshold'])
        histthreshFrame.grid(row=0, column=0, sticky=W + E + N + S)

        histthreshInput = func.buildEntry(obj=self,
                                          root=histthreshFrame,
                                          textvariable=self.plot_TempThresh)
        histthreshInput.insert(END, 200)
        histthreshInput.pack()

        frameRangeFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.plotOptionsFrame,
                                                    label='Frame Range')

        ToolTip.createToolTip(frameRangeFrame, self.descriptions['range'])
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

    def buildGradOptionsFrame(self):
        self.gradFrame = func.buildOuterLabelFrame(obj=self,
                                                   root=self.optionsPanel,
                                                   label='Gradient Plots')

        self.gradFrame.pack(fill=BOTH)

        emptyFrame = Frame(self.gradFrame, bg=self.ACTIVEBACKGROUND)
        emptyFrame.pack(anchor=CENTER)

        gradMagFrame = func.buildInnerLabelFrame(
            obj=self, root=emptyFrame, label='Gradient Magnitude Plot')
        gradMagFrame.grid(row=0, column=0)

        gradMagCheckButton = func.buildFlagCheckButton(obj=self,
                                                       root=gradMagFrame,
                                                       variable=self.grad_mag)
        gradMagCheckButton.pack()

        gradAngleFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=emptyFrame,
                                                   label='Gradient Angle Plot')
        gradAngleFrame.grid(row=0, column=1)

        gradAngleCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradAngleFrame, variable=self.grad_angle)
        gradAngleCheckButton.pack()

        grad2dHistFrame = func.buildInnerLabelFrame(
            obj=self, root=emptyFrame, label='Gradient 2D Histogram')
        grad2dHistFrame.grid(row=0, column=2)

        grad2dHistCheckButton = func.buildFlagCheckButton(
            obj=self, root=grad2dHistFrame, variable=self.grad_2dHist)
        grad2dHistCheckButton.pack()

        gradScatterFrame = func.buildInnerLabelFrame(
            obj=self, root=emptyFrame, label='Gradient Scatter Plot')
        gradScatterFrame.grid(row=1, column=0)

        gradScatterCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradScatterFrame, variable=self.grad_scatter)
        gradScatterCheckButton.pack()

        gradHexBinFrame = func.buildInnerLabelFrame(
            obj=self, root=emptyFrame, label='Gradient Hex Bin Plot')
        gradHexBinFrame.grid(row=1, column=1)

        gradHexBinCheckButton = func.buildFlagCheckButton(
            obj=self, root=gradHexBinFrame, variable=self.grad_hexBin)
        gradHexBinCheckButton.pack()

        grad3dFrame = func.buildInnerLabelFrame(obj=self,
                                                root=emptyFrame,
                                                label='3D Plot')
        grad3dFrame.grid(row=1, column=2)

        grad3dCheckButton = func.buildFlagCheckButton(obj=self,
                                                      root=grad3dFrame,
                                                      variable=self.grad_3D)
        grad3dCheckButton.pack()

        gradAllFrame = func.buildInnerLabelFrame(obj=self,
                                                 root=emptyFrame,
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
                                     command=lambda: handler.create_plots(
                                         self=self,
                                         pixel=(int(self.plot_PixelLocX.get(
                                         )), int(self.plot_PixelLocY.get()))),
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
                        value=buttons[key],
                        bg=self.ACTIVEBACKGROUND,
                        bd=0,
                        highlightthickness=0).pack()

        return radio_frame
