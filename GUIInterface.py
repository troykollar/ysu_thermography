from tkinter import *
import GUIHandler as handler


class GUI:

    def __init__(self):
        self.BACKGROUND = '#FFFFFF'
        self.BUTTONBACKGROUND = 'deep sky blue'
        self.FRAMEBORDER = 'light sky blue'

        self.root = Tk()
        self.root.title("YSU Thermography")
        self.root['bg'] = self.BACKGROUND
        # root.iconbitmap("images/YSU_Logo")

        # Creating variables for checkboxes to change
        self.generateImg = BooleanVar()
        self.saveFrame = BooleanVar()
        self.playVideo = BooleanVar()
        self.saveVideo = BooleanVar()
        self.genThresholdImg = BooleanVar()
        self.dataSet = BooleanVar()
        self.gradientHistogram = BooleanVar()
        self.pixelTempRange = BooleanVar()
        self.play_disp_mp = BooleanVar()
        self.play_top_ref = BooleanVar()
        self.play_bot_ref = BooleanVar()

        # Creating Frame Sections
        self.filePanel = Frame(self.root, bg=self.BACKGROUND)
        self.filePanel.pack(side=TOP, fill=X, pady=10)
        self.optionsPanel = Frame(self.root, bg=self.BACKGROUND)
        self.optionsPanel.pack(fill=X)
        self.buttonPanel = Frame(self.root, bg=self.BACKGROUND)
        self.buttonPanel.pack(side=BOTTOM, fill=X)

        # Building  all frames
        self.buildFileFrame()
        self.buildFunctionFrame()
        self.buildThresholdImageFrame()
        self.buildSaveImageFrame()
        self.buildPlaySaveFrame()
        self.buildPlotOptionsFrame()
        self.buildButtonFrame()

        # Main GUI loop
        self.root.mainloop()

    def buildFileFrame(self):
        tempDataLabel = Label(self.filePanel, text="File Path Build Data Folder: ")
        tempDataLabel.pack(side=LEFT)
        tempDataEntry = Entry(self.filePanel, width=100,
                              relief=FLAT)
        tempDataEntry.pack(side=LEFT)

        tempDataBrowse = Button(self.filePanel, text="Browse", command=lambda: handler.browseFiles(self, tempDataEntry),
                                bd=2, bg=self.BUTTONBACKGROUND, relief=FLAT)
        tempDataBrowse.pack(side=LEFT)

    def buildFunctionFrame(self):
        # Main Frame
        functionsFrame = LabelFrame(self.optionsPanel, text="Functions", bg=self.BACKGROUND,
                                    bd=1)
        functionsFrame.pack(fill=X, ipady=5, pady=10)

        # Frame to hold checkbox to create a threshold image
        genThresholdImgLabel = LabelFrame(functionsFrame, text="Gen Threshold Img",
                                          bd=0, highlightthickness=0, bg=self.BACKGROUND)
        genThresholdImgLabel.pack(side=LEFT, expand=1)
        genThresholdImgCheckbox = Checkbutton(genThresholdImgLabel, variable=self.genThresholdImg,
                                              bg=self.BACKGROUND)
        genThresholdImgCheckbox.pack()

        # Frame to hold checkbox to save a frame
        saveFrameLabel = LabelFrame(functionsFrame, text="Save Frame",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND)
        saveFrameLabel.pack(side=LEFT, expand=1)
        saveFrameCheckbox = Checkbutton(saveFrameLabel, variable=self.saveFrame,
                                        bg=self.BACKGROUND)
        saveFrameCheckbox.pack()

        # Frame to hold checkbox to play video
        playVideoLabel = LabelFrame(functionsFrame, text="Play Video",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND)
        playVideoLabel.pack(side=LEFT, expand=1)
        playVideoCheckbox = Checkbutton(playVideoLabel, variable=self.playVideo,
                                        bg=self.BACKGROUND)
        playVideoCheckbox.pack()

        saveVideoLabel = LabelFrame(functionsFrame, text="Save Video",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND)
        saveVideoLabel.pack(side=LEFT, expand=1)
        saveVideoCheckbox = Checkbutton(saveVideoLabel, variable=self.saveVideo,
                                        bg=self.BACKGROUND)
        saveVideoCheckbox.pack()

        gradientHistogramLabel = LabelFrame(functionsFrame, text="Gradient Histogram",
                                            bd=0, highlightthickness=0, bg=self.BACKGROUND)
        gradientHistogramLabel.pack(side=LEFT, expand=1)
        gradientHistogramCheckbox = Checkbutton(gradientHistogramLabel, variable=self.gradientHistogram,
                                                bg=self.BACKGROUND)
        gradientHistogramCheckbox.pack()

        pixelTempRangeLabel = LabelFrame(functionsFrame, text="Pixel Temp Line Plot",
                                         bd=0, highlightthickness=0, bg=self.BACKGROUND)
        pixelTempRangeLabel.pack(side=LEFT, expand=1)
        pixelTempRangeCheckbox = Checkbutton(pixelTempRangeLabel, variable=self.pixelTempRange,
                                             bg=self.BACKGROUND)
        pixelTempRangeCheckbox.pack()

    def buildThresholdImageFrame(self):
        genThresholdImgFrame = LabelFrame(self.optionsPanel, text="Threshold Image Options",
                                          bg=self.BACKGROUND)
        genThresholdImgFrame.pack(fill=X)

        thresholdFrame = LabelFrame(genThresholdImgFrame, text="Temperature Threshold")
        thresholdFrame.pack(side=LEFT, expand=1)
        genthreshold_thresholdInput = Entry(thresholdFrame, width=3)
        genthreshold_thresholdInput.pack()

    def buildSaveImageFrame(self):
        saveFrameFrame = LabelFrame(self.optionsPanel, text="Save Frame Options",
                                    bg=self.BACKGROUND)
        saveFrameFrame.pack(fill=X)

        frameFrame = LabelFrame(saveFrameFrame, text="Frame")
        frameFrame.pack(side=LEFT, expand=1)
        frameInput = Entry(frameFrame)
        frameInput.pack()

        destDataLabel = LabelFrame(saveFrameFrame, text="Image Number")
        destDataLabel.pack(side=LEFT)
        destDataEntry = Entry(destDataLabel, width=3)
        destDataEntry.insert(END, 1)
        destDataEntry.pack()

    def buildPlaySaveFrame(self):
        playVideoFrame = LabelFrame(self.optionsPanel, text="Play and Save Video Options",
                                    bg=self.BACKGROUND)
        playVideoFrame.pack(fill=X, ipady=10)

        scaleFactorFrame = LabelFrame(playVideoFrame, text="Scale Factor",
                                      padx=7)
        scaleFactorFrame.pack(side=LEFT, expand=1)
        play_scaleFactorInput = Entry(scaleFactorFrame, width=2)
        play_scaleFactorInput.insert(END, 1)
        play_scaleFactorInput.pack()

        frameDelayFrame = LabelFrame(playVideoFrame, text="Frame Delay (for play video)",
                                     padx=7)
        frameDelayFrame.pack(side=LEFT, expand=1)
        play_frameDelayInput = Entry(frameDelayFrame, width=2)
        play_frameDelayInput.insert(END, 1)
        play_frameDelayInput.pack()

        fmaxFrame = LabelFrame(playVideoFrame, text="# pixels around max temp",
                               padx=7)
        fmaxFrame.pack(side=LEFT, expand=1)
        play_fmaxInput = Entry(fmaxFrame, width=3)
        play_fmaxInput.insert(END, False)
        play_fmaxInput.pack()

        cthreshFrame = LabelFrame(playVideoFrame, text="Contour Temp Thresh",
                                  padx=7)
        cthreshFrame.pack(side=LEFT, expand=1)
        play_cthreshInput = Entry(cthreshFrame, width=3)
        play_cthreshInput.insert(END, 0)
        play_cthreshInput.pack()

        fcontourFrame = LabelFrame(playVideoFrame, text="Contour Pixel Range",
                                   padx=7)
        fcontourFrame.pack(side=LEFT, expand=1)
        play_fcontourInput = Entry(fcontourFrame, width=3)
        play_fcontourInput.insert(END, False)
        play_fcontourInput.pack()

        mpFrame = LabelFrame(playVideoFrame, text="Display Meltpool",
                             padx=7)
        mpFrame.pack(side=LEFT, expand=1)
        play_mpInput = Checkbutton(mpFrame, variable=self.play_disp_mp)
        play_mpInput.pack()

        toprefFrame = LabelFrame(playVideoFrame, text="Remove Top Reflection",
                                 padx=7)
        toprefFrame.pack(side=LEFT, expand=1)
        play_toprefInput = Checkbutton(toprefFrame, variable=self.play_top_ref)
        play_toprefInput.pack()

        botrefFrame = LabelFrame(playVideoFrame, text="Remove Bottom Reflection",
                                 padx=7)
        botrefFrame.pack(side=LEFT, expand=1)
        play_botrefInput = Checkbutton(botrefFrame, variable=self.play_bot_ref)
        play_botrefInput.pack()

        fpsFrame = LabelFrame(playVideoFrame, text="Framerate (For Save Video Only)",
                              padx=7)
        fpsFrame.pack(side=LEFT, expand=1)
        save_fpsInput = Entry(fpsFrame, width=3)
        save_fpsInput.insert(END, 60)
        save_fpsInput.pack()

    def buildPlotOptionsFrame(self):
        plotOptionsFrame = LabelFrame(self.optionsPanel, text="Plot options",
                                      bg=self.BACKGROUND)
        plotOptionsFrame.pack(fill=X)

        pixelLocationFrame = LabelFrame(plotOptionsFrame, text="Pixel Location")
        pixelLocationFrame.pack(side=LEFT, expand=1)
        pixelXLocationInput = Entry(pixelLocationFrame, width=4)
        pixelXLocationInput.pack(side=LEFT)
        comma = Label(pixelLocationFrame, text=",")
        comma.pack(side=LEFT)
        pixelYLocationInput = Entry(pixelLocationFrame, width=4)
        pixelYLocationInput.pack(side=LEFT)

        histthreshFrame = LabelFrame(plotOptionsFrame, text="Temperature Threshold (histogram)")
        histthreshFrame.pack(side=LEFT, expand=1)
        histthreshInput = Entry(histthreshFrame, width=4)
        histthreshInput.insert(END, 200)
        histthreshInput.pack()

        histBinFrame = LabelFrame(plotOptionsFrame, text="Bin Count (histogram)")
        histBinFrame.pack(side=LEFT, expand=1)
        histBinInput = Entry(histBinFrame, width=3)
        histBinInput.insert(END, 5)
        histBinInput.pack()

        histGradSpacingFrame = LabelFrame(plotOptionsFrame, text="Gradient Spacing (histogram)")
        histGradSpacingFrame.pack(side=LEFT, expand=1)
        histGradSpacingInput = Entry(histGradSpacingFrame, width=3)
        histGradSpacingInput.insert(END, 1)
        histGradSpacingInput.pack()

        frameRangeFrame = LabelFrame(plotOptionsFrame, text="Frame Range (line plot)")
        frameRangeFrame.pack(side=LEFT, expand=1)
        plotStartFrameInput = Entry(frameRangeFrame, width=5)
        plotStartFrameInput.insert(END, 0)
        plotStartFrameInput.pack()

        plotEndFrameInput = Entry(frameRangeFrame, width=5)
        plotEndFrameInput.insert(END, -1)
        plotEndFrameInput.pack()

    def buildButtonFrame(self):
        closeButton = Button(self.buttonPanel, text="Close", command=self.root.quit,
                             bg=self.BUTTONBACKGROUND, relief=FLAT)
        closeButton.pack(side=LEFT)

        submitButton = Button(self.buttonPanel, text="Submit", command=lambda: handler.submit(self=self),
                              bg=self.BUTTONBACKGROUND, relief=FLAT)
        submitButton.pack(side=RIGHT)

