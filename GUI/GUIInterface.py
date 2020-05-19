from tkinter import *
from GUI import Descriptors, ToolTip
from GUI import GUIHandler as handler
import GUI.constants as consts
from GUI import helper_functions as func


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
        self.select_pixels = BooleanVar()

        # Creating Frame Sections
        self.filePanel = Frame(self.root, bg=self.ACTIVEBACKGROUND)
        self.filePanel.pack(side=TOP, fill=BOTH, pady=10)
        self.optionsPanel = Frame(self.root, bg=self.ACTIVEBACKGROUND, bd=1, highlightthickness=1,
                                  highlightcolor=self.ACTIVEFRAMEBORDER, highlightbackground=self.ACTIVEFRAMEBORDER,
                                  padx=5, relief=FLAT)
        self.optionsPanel.pack(fill=BOTH)

        self.optionsPanel.columnconfigure(0, weight=1)
        self.optionsPanel.columnconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(0, weight=1)
        self.optionsPanel.rowconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(2, weight=1)
        self.optionsPanel.rowconfigure(3, weight=1)

        self.buttonPanel = Frame(self.root, bg=self.ACTIVEBACKGROUND)
        self.buttonPanel.pack(side=BOTTOM, fill=X)

        # Building  all frames
        self.buildFileFrame()
        self.buildFunctionFrame()
        self.buildThresholdImageFrame()
        self.buildSaveImageFrame()
        self.buildPlaySaveFrame()
        self.buildPlotOptionsFrame()
        self.buildButtonFrame()

        self.activatePanels()

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

    def activatePanels(self):
        if self.gen_threshold_img.get():
            func.enableChildren(self.genThresholdImgFrame)
        else:
            func.disableChildren(self.genThresholdImgFrame)

        if self.save_frame.get():
            func.enableChildren(self.saveFrameFrame)
        else:
            func.disableChildren(self.saveFrameFrame)

        if self.play_video.get() or self.save_video.get():
            func.enableChildren(self.playVideoFrame)
        else:
            func.disableChildren(self.playVideoFrame)

        if self.gradient_plots.get() or self.pixel_temp_range.get():
            func.enableChildren(self.plotOptionsFrame)
        else:
            func.disableChildren(self.plotOptionsFrame)

        if self.gradient_plots.get():
            func.enableChildren(self.gradFrame)
        else:
            func.disableChildren(self.gradFrame)

    def buildFileFrame(self):
        tempDataLabel = Label(self.filePanel, text="File Path Build Data Folder: ",
                              padx=0, pady=0, bg=self.ACTIVEBACKGROUND, foreground=self.TEXTCOLOR)
        tempDataHint = Descriptors.getHintTextFileFrame('tempDataLabel')
        ToolTip.createToolTip(tempDataLabel, tempDataHint)
        tempDataLabel.pack(side=LEFT)
        tempDataEntry = Entry(self.filePanel, width=75, textvariable=self.tempData,
                              relief=FLAT, bg=self.ACTIVEFIELDBACKGROUND, foreground=self.TEXTCOLOR)
        tempDataEntry.pack(side=LEFT)

        tempDataBrowse = Button(self.filePanel, text="Browse", command=lambda: handler.browseFiles(self, tempDataEntry),
                                bd=2, bg=self.ACTIVEBUTTONBACKGROUND, relief=FLAT, padx=0, pady=0,
                                activeforeground=self.TEXTCOLOR, foreground=self.TEXTCOLOR)
        tempDataBrowse.pack(side=LEFT)

    def buildFunctionFrame(self):
        # Main Frame
        functionsFrame = func.buildOuterLabelFrame(obj=self,
                                                   root=self.optionsPanel,
                                                   label='Functions')

        functionsFrame.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S, ipady=5, pady=5)

        functionsFrame.columnconfigure(0, weight=1)
        functionsFrame.columnconfigure(1, weight=1)
        functionsFrame.columnconfigure(2, weight=1)
        functionsFrame.rowconfigure(0, weight=1)
        functionsFrame.rowconfigure(1, weight=1)

        # Frame to hold checkbox to create a threshold image
        genThresholdImgLabel = func.buildInnerLabelFrame(obj=self,
                                                         root=functionsFrame,
                                                         label='Gen Thresh Image')

        genThresholdImgHint = Descriptors.getHintTextFunctionFrame('genThresholdImgLabel')
        ToolTip.createToolTip(genThresholdImgLabel, genThresholdImgHint)
        genThresholdImgLabel.grid(row=0, column=0, sticky=W + E + N + S)

        genThresholdImgCheckbox = func.buildFunctionCheckButton(obj=self,
                                                                root=genThresholdImgLabel,
                                                                variable=self.gen_threshold_img,
                                                                command=self.activatePanels)
        genThresholdImgCheckbox.pack()

        # Frame to hold checkbox to save a frame
        saveFrameLabel = func.buildInnerLabelFrame(obj=self,
                                                   root=functionsFrame,
                                                   label='Save Frame')

        saveFrameHint = Descriptors.getHintTextFunctionFrame('saveFrameLabel')
        ToolTip.createToolTip(saveFrameLabel, saveFrameHint)
        saveFrameLabel.grid(row=0, column=1, sticky=W + E + N + S)

        saveFrameCheckbox = func.buildFunctionCheckButton(obj=self,
                                                          root=saveFrameLabel,
                                                          variable=self.save_frame,
                                                          command=self.activatePanels)
        saveFrameCheckbox.pack()

        # Frame to hold checkbox to play video
        playVideoLabel = func.buildInnerLabelFrame(obj=self,
                                                   root=functionsFrame,
                                                   label='Play Video')

        playVideoHint = Descriptors.getHintTextFunctionFrame('playVideoLabel')
        ToolTip.createToolTip(playVideoLabel, playVideoHint)
        playVideoLabel.grid(row=0, column=2, sticky=W + E + N + S)

        playVideoCheckbox = func.buildFunctionCheckButton(obj=self,
                                                          root=playVideoLabel,
                                                          variable=self.play_video,
                                                          command=self.activatePanels)
        playVideoCheckbox.pack()

        # Frame to Hold Option to Save Video
        saveVideoLabel = func.buildInnerLabelFrame(obj=self,
                                                   root=functionsFrame,
                                                   label='Save Video')

        saveVideoHint = Descriptors.getHintTextFunctionFrame('saveVideoLabel')
        ToolTip.createToolTip(saveVideoLabel, saveVideoHint)
        saveVideoLabel.grid(row=1, column=0, sticky=W + E + N + S)

        saveVideoCheckbox = func.buildFunctionCheckButton(obj=self,
                                                          root=saveVideoLabel,
                                                          variable=self.save_video,
                                                          command=self.activatePanels)
        saveVideoCheckbox.pack()

        # Frame to Hold Option to Plot Gradient Info
        gradientHistogramLabel = func.buildInnerLabelFrame(obj=self,
                                                           root=functionsFrame,
                                                           label='Gradient Plots')

        gradientHistogramHint = Descriptors.getHintTextFunctionFrame('gradientHistogramLabel')
        ToolTip.createToolTip(gradientHistogramLabel, gradientHistogramHint)
        gradientHistogramLabel.grid(row=1, column=1, sticky=W + E + N + S)

        gradientHistogramCheckbox = func.buildFunctionCheckButton(obj=self,
                                                                  root=gradientHistogramLabel,
                                                                  variable=self.gradient_plots,
                                                                  command=self.activatePanels)
        gradientHistogramCheckbox.pack()

        # Frame to Hold Option to Plot Temporal Data
        pixelTempRangeLabel = func.buildInnerLabelFrame(obj=self,
                                                        root=functionsFrame,
                                                        label='Temp Line Plot')

        pixelTempRangeHint = Descriptors.getHintTextFunctionFrame('pixelTempRangeLabel')
        ToolTip.createToolTip(pixelTempRangeLabel, pixelTempRangeHint)
        pixelTempRangeLabel.grid(row=1, column=2, sticky=W + E + N + S)

        pixelTempRangeCheckbox = func.buildFunctionCheckButton(obj=self,
                                                               root=pixelTempRangeLabel,
                                                               variable=self.pixel_temp_range,
                                                               command=self.activatePanels)
        pixelTempRangeCheckbox.pack()

    def buildThresholdImageFrame(self):
        self.genThresholdImgFrame = func.buildOuterLabelFrame(obj=self,
                                                              root=self.optionsPanel,
                                                              label='Threshold Image Options')

        self.genThresholdImgFrame.grid(row=1, column=0, sticky=W + E + N + S, ipady=5, pady=5, padx=5)

        thresholdFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=self.genThresholdImgFrame,
                                                   label='Temperature Threshold')

        thresholdHint = Descriptors.getHintTextThresholdFrame('thresholdFrame')
        ToolTip.createToolTip(thresholdFrame, thresholdHint)
        thresholdFrame.pack(side=LEFT, expand=1)

        genthreshold_thresholdInput = func.buildEntry(obj=self,
                                                      root=thresholdFrame,
                                                      textvariable=self.genthreshold_threshold)
        genthreshold_thresholdInput.pack()

    def buildSaveImageFrame(self):
        self.saveFrameFrame = func.buildOuterLabelFrame(obj=self,
                                                        root=self.optionsPanel,
                                                        label='Save Frame Options')

        self.saveFrameFrame.grid(row=1, column=1, sticky=W + E + N + S)

        frameFrame = func.buildInnerLabelFrame(obj=self,
                                               root=self.saveFrameFrame,
                                               label='Frame Number')

        frameHint = Descriptors.getHintTextSaveImageFrame('frameFrame')
        ToolTip.createToolTip(frameFrame, frameHint)
        frameFrame.pack(side=LEFT, expand=1)

        frameInput = func.buildEntry(obj=self,
                                     root=frameFrame,
                                     width=10,
                                     textvariable=self.save_FrameNumber)
        frameInput.pack()

        destDataLabel = func.buildInnerLabelFrame(obj=self,
                                                  root=self.saveFrameFrame,
                                                  label='Image Title')

        destHint = Descriptors.getHintTextSaveImageFrame('destDataLabel')
        ToolTip.createToolTip(destDataLabel, destHint)
        destDataLabel.pack(side=LEFT, expand=1)

        destDataEntry = func.buildEntry(obj=self,
                                        root=destDataLabel,
                                        width=10,
                                        textvariable=self.save_ImageNumber)
        destDataEntry.insert(END, 1)
        destDataEntry.pack()

    def buildPlaySaveFrame(self):
        self.playVideoFrame = func.buildOuterLabelFrame(obj=self,
                                                        root=self.optionsPanel,
                                                        label='Play and Save Video Options')

        self.playVideoFrame.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S, ipady=7)

        self.playVideoFrame.columnconfigure(0, weight=1)
        self.playVideoFrame.columnconfigure(1, weight=1)
        self.playVideoFrame.columnconfigure(2, weight=1)
        self.playVideoFrame.rowconfigure(0, weight=1)
        self.playVideoFrame.rowconfigure(1, weight=1)
        self.playVideoFrame.rowconfigure(2, weight=1)
        self.playVideoFrame.rowconfigure(3, weight=1)

        scaleFactorFrame = func.buildInnerLabelFrame(obj=self,
                                                     root=self.playVideoFrame,
                                                     label='Scale Factor')

        scaleFactorHint = Descriptors.getHintTextSavePlayFrame('scaleFactorFrame')
        ToolTip.createToolTip(scaleFactorFrame, scaleFactorHint)
        scaleFactorFrame.grid(row=0, column=0, sticky=W + E + N + S)

        play_scaleFactorInput = func.buildEntry(obj=self,
                                                root=scaleFactorFrame,
                                                textvariable=self.play_scaleFactor)
        play_scaleFactorInput.insert(END, 1)
        play_scaleFactorInput.pack()

        frameDelayFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.playVideoFrame,
                                                    label='Frame Delay (For Play Video)')

        frameDelayHint = Descriptors.getHintTextSavePlayFrame('frameDelayFrame')
        ToolTip.createToolTip(frameDelayFrame, frameDelayHint)
        frameDelayFrame.grid(row=0, column=1, sticky=W + E + N + S)

        play_frameDelayInput = func.buildEntry(obj=self,
                                               root=frameDelayFrame,
                                               textvariable=self.play_frameDelay)
        play_frameDelayInput.insert(END, 1)
        play_frameDelayInput.pack()

        fmaxFrame = func.buildInnerLabelFrame(obj=self,
                                              root=self.playVideoFrame,
                                              label='# of Pixels to Display Around Max Temp')

        fmaxHint = Descriptors.getHintTextSavePlayFrame('fmaxFrame')
        ToolTip.createToolTip(fmaxFrame, fmaxHint)
        fmaxFrame.grid(row=0, column=2, sticky=W + E + N + S)

        play_fmaxInput = func.buildEntry(obj=self,
                                         root=fmaxFrame,
                                         textvariable=self.play_pixelAroundMax)
        play_fmaxInput.insert(END, False)
        play_fmaxInput.pack()

        cthreshFrame = func.buildInnerLabelFrame(obj=self,
                                                 root=self.playVideoFrame,
                                                 label='Contour Temperature Threshold')

        cthreshHint = Descriptors.getHintTextSavePlayFrame('cthreshFrame')
        ToolTip.createToolTip(cthreshFrame, cthreshHint)
        cthreshFrame.grid(row=1, column=0, sticky=W + E + N + S)

        play_cthreshInput = func.buildEntry(obj=self,
                                            root=cthreshFrame,
                                            textvariable=self.play_contourTempThresh)
        play_cthreshInput.insert(END, 0)
        play_cthreshInput.pack()

        fcontourFrame = func.buildInnerLabelFrame(obj=self,
                                                  root=self.playVideoFrame,
                                                  label='Contour Size (in Pixels)')

        fcontourHint = Descriptors.getHintTextSavePlayFrame('fcontourFrame')
        ToolTip.createToolTip(fcontourFrame, fcontourHint)
        fcontourFrame.grid(row=1, column=1, sticky=W + E + N + S)

        play_fcontourInput = func.buildEntry(obj=self,
                                             root=fcontourFrame,
                                             textvariable=self.play_contourPixelRange)
        play_fcontourInput.insert(END, False)
        play_fcontourInput.pack()

        fpsFrame = func.buildInnerLabelFrame(obj=self,
                                             root=self.playVideoFrame,
                                             label='FPS (For Saved Video)')

        fpsHint = Descriptors.getHintTextSavePlayFrame('fpsFrame')
        ToolTip.createToolTip(fpsFrame, fpsHint)
        fpsFrame.grid(row=1, column=2, sticky=W + E + N + S)

        save_fpsInput = func.buildEntry(obj=self,
                                        root=fpsFrame,
                                        textvariable=self.play_frameRate)
        save_fpsInput.insert(END, 60)
        save_fpsInput.pack()

        toprefFrame = func.buildInnerLabelFrame(obj=self,
                                                root=self.playVideoFrame,
                                                label='Remove Top Reflection')
        toprefHint = Descriptors.getHintTextSavePlayFrame('toprefFrame')
        ToolTip.createToolTip(toprefFrame, toprefHint)
        toprefFrame.grid(row=2, column=0, sticky=W + E + N + S)
        play_toprefInput = func.buildFlagCheckButton(obj=self,
                                                     root=toprefFrame,
                                                     variable=self.play_removeTopReflection)
        play_toprefInput.pack()

        botrefFrame = func.buildInnerLabelFrame(obj=self,
                                                root=self.playVideoFrame,
                                                label='Remove Bottom Reflection')

        botrefHint = Descriptors.getHintTextSavePlayFrame('botrefFrame')
        ToolTip.createToolTip(botrefFrame, botrefHint)
        botrefFrame.grid(row=2, column=1, sticky=W + E + N + S)
        play_botrefInput = func.buildFlagCheckButton(obj=self,
                                                     root=botrefFrame,
                                                     variable=self.play_removeBottomReflection)
        play_botrefInput.pack()

        mpFrame = func.buildInnerLabelFrame(obj=self,
                                            root=self.playVideoFrame,
                                            label='Display Meltpool Info')

        mpHint = Descriptors.getHintTextSavePlayFrame('mpFrame')
        ToolTip.createToolTip(mpFrame, mpHint)
        mpFrame.grid(row=2, column=2, sticky=W + E + N + S)

        play_mpInput = func.buildFlagCheckButton(obj=self,
                                                 root=mpFrame,
                                                 variable=self.play_displayMeltPool)
        play_mpInput.pack()

        frameRangeFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.playVideoFrame,
                                                    label='Frame Range (For Saved Video)')

        frameRangeHint = Descriptors.getHintTextSavePlayFrame('frameRangeFrame')
        ToolTip.createToolTip(frameRangeFrame, frameRangeHint)
        frameRangeFrame.grid(row=3, column=1, sticky=W + E + N + S)

        frameRangeFrame.columnconfigure(0, weight=1)
        frameRangeFrame.columnconfigure(1, weight=1)
        frameRangeFrame.rowconfigure(0, weight=1)

        saveStartFrameInput = func.buildEntry(obj=self,
                                              root=frameRangeFrame,
                                              textvariable=self.play_saveStartFrame)
        saveStartFrameInput.insert(END, 0)
        saveStartFrameInput.grid(row=0, column=0)

        saveEndFrameInput = func.buildEntry(obj=self,
                                            root=frameRangeFrame,
                                            textvariable=self.play_saveEndFrame)
        saveEndFrameInput.insert(END, -1)
        saveEndFrameInput.grid(row=0, column=1)

        contourOnImgFrame = func.buildInnerLabelFrame(obj=self,
                                                      root=self.playVideoFrame,
                                                      label='Display Contour')
        contourOnImgHint = Descriptors.getHintTextSavePlayFrame('contourOnImgFrame')
        ToolTip.createToolTip(contourOnImgFrame, contourOnImgHint)
        contourOnImgFrame.grid(row=3, column=2, sticky=W + E + N + S)
        contourOnImgInput = func.buildFlagCheckButton(obj=self,
                                                      root=contourOnImgFrame,
                                                      variable=self.play_displayContour)
        contourOnImgInput.pack()

    def buildPlotOptionsFrame(self):
        self.plotOptionsFrame = func.buildOuterLabelFrame(obj=self,
                                                          root=self.optionsPanel,
                                                          label='Plot Options')

        self.plotOptionsFrame.grid(row=3, column=0, columnspan=2, sticky=W + E + N + S)

        self.plotOptionsFrame.columnconfigure(0, weight=1)
        self.plotOptionsFrame.columnconfigure(1, weight=1)
        self.plotOptionsFrame.columnconfigure(2, weight=1)
        self.plotOptionsFrame.rowconfigure(0, weight=1)
        self.plotOptionsFrame.rowconfigure(1, weight=1)
        self.plotOptionsFrame.rowconfigure(2, weight=1)

        pixelLocationFrame = func.buildInnerLabelFrame(obj=self,
                                                       root=self.plotOptionsFrame,
                                                       label='Pixel Location')

        pixelLocationHint = Descriptors.getHintTextPlotOptions('pixelLocationFrame')
        ToolTip.createToolTip(pixelLocationFrame, pixelLocationHint)
        pixelLocationFrame.grid(row=0, column=1, sticky=W + E + N + S)

        pixelLocationFrame.columnconfigure(0, weight=1)
        pixelLocationFrame.columnconfigure(1, weight=1)
        pixelLocationFrame.columnconfigure(2, weight=1)
        pixelLocationFrame.rowconfigure(0, weight=1)

        pixelXLocationInput = func.buildEntry(obj=self,
                                              root=pixelLocationFrame,
                                              textvariable=self.plot_PixelLocX)

        pixelXLocationInput.grid(row=0, column=0, sticky=W + E + N + S)
        comma = Label(pixelLocationFrame, text=",",
                      bd=0, highlightthickness=0, bg=self.ACTIVEBACKGROUND)
        comma.grid(row=0, column=1, sticky=W + E + N + S)
        pixelYLocationInput = func.buildEntry(obj=self,
                                              root=pixelLocationFrame,
                                              textvariable=self.plot_PixelLocY)

        pixelYLocationInput.grid(row=0, column=2, sticky=W + E + N + S)

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

        plotStartFrameInput = func.buildEntry(obj=self,
                                              root=frameRangeFrame,
                                              textvariable=self.plot_StartFrame)
        plotStartFrameInput.insert(END, 0)
        plotStartFrameInput.grid(row=0, column=0)

        plotEndFrameInput = func.buildEntry(obj=self,
                                            root=frameRangeFrame,
                                            textvariable=self.plot_EndFrame)
        plotEndFrameInput.insert(END, -1)
        plotEndFrameInput.grid(row=0, column=1)

        self.selectPixelsFrame = func.buildInnerLabelFrame(obj=self,
                                                           root=self.plotOptionsFrame,
                                                           label='Create Composite and select pixels')
        self.selectPixelsFrame.grid(row=1, column=1)

        selectPixelCheckButton = func.buildFlagCheckButton(obj=self,
                                                           root=self.selectPixelsFrame,
                                                           variable=self.select_pixels)
        selectPixelCheckButton.pack()

        self.gradFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=self.plotOptionsFrame,
                                                   label='Gradient Plots')

        self.gradFrame.grid(row=3, column=0, columnspan=3)

        gradMagFrame = func.buildInnerLabelFrame(obj=self,
                                                 root=self.gradFrame,
                                                 label='Gradient Magnitude Plot')
        gradMagFrame.grid(row=0, column=0)

        gradMagCheckButton = func.buildFlagCheckButton(obj=self,
                                                       root=gradMagFrame,
                                                       variable=self.grad_mag)
        gradMagCheckButton.pack()

        gradAngleFrame = func.buildInnerLabelFrame(obj=self,
                                                   root=self.gradFrame,
                                                   label='Gradient Angle Plot')
        gradAngleFrame.grid(row=0, column=1)

        gradAngleCheckButton = func.buildFlagCheckButton(obj=self,
                                                         root=gradAngleFrame,
                                                         variable=self.grad_angle)
        gradAngleCheckButton.pack()

        grad2dHistFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.gradFrame,
                                                    label='Gradient 2D Histogram')
        grad2dHistFrame.grid(row=0, column=2)

        grad2dHistCheckButton = func.buildFlagCheckButton(obj=self,
                                                          root=grad2dHistFrame,
                                                          variable=self.grad_2dHist)
        grad2dHistCheckButton.pack()

        gradScatterFrame = func.buildInnerLabelFrame(obj=self,
                                                     root=self.gradFrame,
                                                     label='Gradient Scatter Plot')
        gradScatterFrame.grid(row=1, column=0)

        gradScatterCheckButton = func.buildFlagCheckButton(obj=self,
                                                           root=gradScatterFrame,
                                                           variable=self.grad_scatter)
        gradScatterCheckButton.pack()

        gradHexBinFrame = func.buildInnerLabelFrame(obj=self,
                                                    root=self.gradFrame,
                                                    label='Gradient Hex Bin Plot')
        gradHexBinFrame.grid(row=1, column=1)

        gradHexBinCheckButton = func.buildFlagCheckButton(obj=self,
                                                          root=gradHexBinFrame,
                                                          variable=self.grad_hexBin)
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

        gradAllCheckButton = func.buildFunctionCheckButton(obj=self,
                                                           root=gradAllFrame,
                                                           variable=self.grad_all,
                                                           command=self.gradSelectAll)
        gradAllCheckButton.pack()

    def buildButtonFrame(self):
        closeButton = Button(self.buttonPanel, text="Close", command=self.root.quit,
                             bg=self.ACTIVEBUTTONBACKGROUND, relief=FLAT)
        closeButton.pack(side=LEFT)

        submitButton = Button(self.buttonPanel, text="Submit", command=lambda: handler.submit(self=self),
                              bg=self.ACTIVEBUTTONBACKGROUND, relief=FLAT)
        submitButton.pack(side=RIGHT)
