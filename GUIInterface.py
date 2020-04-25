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
        self.filePanel.pack(side=TOP, fill=BOTH, pady=10)
        self.optionsPanel = Frame(self.root, bg=self.BACKGROUND, bd=1, highlightthickness=1,
                                  highlightcolor=self.FRAMEBORDER, highlightbackground=self.FRAMEBORDER,
                                  padx=5, relief=FLAT)
        self.optionsPanel.pack(fill=BOTH)

        self.optionsPanel.columnconfigure(0, weight=1)
        self.optionsPanel.columnconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(0, weight=1)
        self.optionsPanel.rowconfigure(1, weight=1)
        self.optionsPanel.rowconfigure(2, weight=1)
        self.optionsPanel.rowconfigure(3, weight=1)

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
        tempDataLabel = Label(self.filePanel, text="File Path Build Data Folder: ",
                              padx=0, pady=0, bg=self.BACKGROUND)
        tempDataLabel.pack(side=LEFT)
        tempDataEntry = Entry(self.filePanel, width=75,
                              relief=FLAT)
        tempDataEntry.pack(side=LEFT)

        tempDataBrowse = Button(self.filePanel, text="Browse", command=lambda: handler.browseFiles(self, tempDataEntry),
                                bd=2, bg=self.BUTTONBACKGROUND, relief=FLAT, padx=0, pady=0,
                                activeforeground=self.FRAMEBORDER)
        tempDataBrowse.pack(side=LEFT)

    def buildFunctionFrame(self):
        # Main Frame
        functionsFrame = LabelFrame(self.optionsPanel, text="Functions", bd=1, highlightthickness=1,
                                    highlightcolor=self.FRAMEBORDER,
                                    highlightbackground=self.FRAMEBORDER, bg=self.BACKGROUND,
                                    padx=5, relief=FLAT)
        functionsFrame.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S, ipady=5, pady=5)

        functionsFrame.columnconfigure(0, weight=1)
        functionsFrame.columnconfigure(1, weight=1)
        functionsFrame.columnconfigure(2, weight=1)
        functionsFrame.rowconfigure(0, weight=1)
        functionsFrame.rowconfigure(1, weight=1)

        # Frame to hold checkbox to create a threshold image
        genThresholdImgLabel = LabelFrame(functionsFrame, text="Gen Threshold Img",
                                          bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                          labelanchor=N, padx=5)
        genThresholdImgLabel.grid(row=0, column=0, sticky=W+E+N+S)
        genThresholdImgCheckbox = Checkbutton(genThresholdImgLabel, variable=self.genThresholdImg,
                                              bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                              activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                              relief=FLAT, highlightcolor=self.BACKGROUND)
        genThresholdImgCheckbox.pack()

        # Frame to hold checkbox to save a frame
        saveFrameLabel = LabelFrame(functionsFrame, text="Save Frame",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                    labelanchor=N, padx=5)
        saveFrameLabel.grid(row=0, column=1, sticky=W+E+N+S)
        saveFrameCheckbox = Checkbutton(saveFrameLabel, variable=self.saveFrame,
                                        bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                        activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                        relief=FLAT, highlightcolor=self.BACKGROUND)
        saveFrameCheckbox.pack()

        # Frame to hold checkbox to play video
        playVideoLabel = LabelFrame(functionsFrame, text="Play Video",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                    labelanchor=N, padx=5)
        playVideoLabel.grid(row=0, column=2, sticky=W+E+N+S)
        playVideoCheckbox = Checkbutton(playVideoLabel, variable=self.playVideo,
                                        bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                        activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                        relief=FLAT, highlightcolor=self.BACKGROUND)
        playVideoCheckbox.pack()

        saveVideoLabel = LabelFrame(functionsFrame, text="Save Video",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                    labelanchor=N, padx=5)
        saveVideoLabel.grid(row=1, column=0, sticky=W+E+N+S)
        saveVideoCheckbox = Checkbutton(saveVideoLabel, variable=self.saveVideo,
                                        bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                        activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                        relief=FLAT, highlightcolor=self.BACKGROUND)
        saveVideoCheckbox.pack()

        gradientHistogramLabel = LabelFrame(functionsFrame, text="Gradient Histogram",
                                            bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                            labelanchor=N, padx=5)
        gradientHistogramLabel.grid(row=1, column=1, sticky=W+E+N+S)
        gradientHistogramCheckbox = Checkbutton(gradientHistogramLabel, variable=self.gradientHistogram,
                                                bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                                activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                                relief=FLAT, highlightcolor=self.BACKGROUND)
        gradientHistogramCheckbox.pack()

        pixelTempRangeLabel = LabelFrame(functionsFrame, text="Pixel Temp Line Plot",
                                         bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                         labelanchor=N, padx=5)
        pixelTempRangeLabel.grid(row=1, column=2, sticky=W+E+N+S)
        pixelTempRangeCheckbox = Checkbutton(pixelTempRangeLabel, variable=self.pixelTempRange,
                                             bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                             activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                             relief=FLAT, highlightcolor=self.BACKGROUND)
        pixelTempRangeCheckbox.pack()

    def buildThresholdImageFrame(self):
        genThresholdImgFrame = LabelFrame(self.optionsPanel, text="Threshold Image Options",
                                          bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                          padx=5, relief=FLAT)
        genThresholdImgFrame.grid(row=1, column=0, sticky=W+E+N+S, ipady=5, pady=5, padx=5)

        thresholdFrame = LabelFrame(genThresholdImgFrame, text="Temperature Threshold",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                    labelanchor=N, padx=5, relief=FLAT)
        thresholdFrame.pack(side=LEFT, expand=1)
        genthreshold_thresholdInput = Entry(thresholdFrame, width=3, justify=CENTER, relief=FLAT)
        genthreshold_thresholdInput.pack()

    def buildSaveImageFrame(self):
        saveFrameFrame = LabelFrame(self.optionsPanel, text="Save Frame Options",
                                    bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                    padx=5, relief=FLAT)
        saveFrameFrame.grid(row=1, column=1, sticky=W+E+N+S)

        frameFrame = LabelFrame(saveFrameFrame, text="Frame",
                                bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                labelanchor=N, padx=5, relief=FLAT)
        frameFrame.pack(side=LEFT, expand=1)
        frameInput = Entry(frameFrame, justify=CENTER, relief=FLAT)
        frameInput.pack()

        destDataLabel = LabelFrame(saveFrameFrame, text="Image Number",
                                   bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                   padx=5, relief=FLAT)
        destDataLabel.pack(side=LEFT, expand=1)
        destDataEntry = Entry(destDataLabel, width=3, justify=CENTER, relief=FLAT)
        destDataEntry.insert(END, 1)
        destDataEntry.pack()

    def buildPlaySaveFrame(self):
        playVideoFrame = LabelFrame(self.optionsPanel, text="Play and Save Video Options",
                                    bd=1, highlightthickness=1, highlightcolor=self.FRAMEBORDER,
                                    highlightbackground=self.FRAMEBORDER, bg=self.BACKGROUND,
                                    padx=5, relief=FLAT)
        playVideoFrame.grid(row=2, column=0, columnspan=2, sticky=W+E+N+S, ipady=7)

        playVideoFrame.columnconfigure(0, weight=1)
        playVideoFrame.columnconfigure(1, weight=1)
        playVideoFrame.columnconfigure(2, weight=1)
        playVideoFrame.rowconfigure(0, weight=1)
        playVideoFrame.rowconfigure(1, weight=1)
        playVideoFrame.rowconfigure(2, weight=1)

        scaleFactorFrame = LabelFrame(playVideoFrame, text="Scale Factor",
                                      bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                      labelanchor=N, padx=5)
        scaleFactorFrame.grid(row=0, column=0, sticky=W+E+N+S)
        play_scaleFactorInput = Entry(scaleFactorFrame, width=2, justify=CENTER, relief=FLAT)
        play_scaleFactorInput.insert(END, 1)
        play_scaleFactorInput.pack()

        frameDelayFrame = LabelFrame(playVideoFrame, text="Frame Delay (for play video)",
                                     bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                     labelanchor=N, padx=5)
        frameDelayFrame.grid(row=0, column=1, sticky=W+E+N+S)
        play_frameDelayInput = Entry(frameDelayFrame, width=2, justify=CENTER, relief=FLAT)
        play_frameDelayInput.insert(END, 1)
        play_frameDelayInput.pack()

        fmaxFrame = LabelFrame(playVideoFrame, text="# pixels around max temp",
                               bd=0, highlightthickness=0, bg=self.BACKGROUND,
                               labelanchor=N, padx=5)
        fmaxFrame.grid(row=0, column=2, sticky=W+E+N+S)
        play_fmaxInput = Entry(fmaxFrame, width=3, justify=CENTER, relief=FLAT)
        play_fmaxInput.insert(END, False)
        play_fmaxInput.pack()

        cthreshFrame = LabelFrame(playVideoFrame, text="Contour Temp Thresh",
                                  bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                  labelanchor=N, padx=5)
        cthreshFrame.grid(row=1, column=0, sticky=W+E+N+S)
        play_cthreshInput = Entry(cthreshFrame, width=3, justify=CENTER, relief=FLAT)
        play_cthreshInput.insert(END, 0)
        play_cthreshInput.pack()

        fcontourFrame = LabelFrame(playVideoFrame, text="Contour Pixel Range",
                                   bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                   labelanchor=N, padx=5)
        fcontourFrame.grid(row=1, column=1, sticky=W+E+N+S)
        play_fcontourInput = Entry(fcontourFrame, width=3, justify=CENTER, relief=FLAT)
        play_fcontourInput.insert(END, False)
        play_fcontourInput.pack()

        fpsFrame = LabelFrame(playVideoFrame, text="Framerate (For Save Video Only)",
                              bd=0, highlightthickness=0, bg=self.BACKGROUND,
                              labelanchor=N, padx=5)
        fpsFrame.grid(row=1, column=2, sticky=W + E + N + S)
        save_fpsInput = Entry(fpsFrame, width=3, justify=CENTER, relief=FLAT)
        save_fpsInput.insert(END, 60)
        save_fpsInput.pack()

        toprefFrame = LabelFrame(playVideoFrame, text="Remove Top Reflection",
                                 bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                 labelanchor=N, padx=5)
        toprefFrame.grid(row=2, column=0, sticky=W+E+N+S)
        play_toprefInput = Checkbutton(toprefFrame, variable=self.play_top_ref,
                                       bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                       activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                       relief=FLAT, highlightcolor=self.BACKGROUND)
        play_toprefInput.pack()

        botrefFrame = LabelFrame(playVideoFrame, text="Remove Bottom Reflection",
                                 bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                 labelanchor=N, padx=5)
        botrefFrame.grid(row=2, column=1, sticky=W+E+N+S)
        play_botrefInput = Checkbutton(botrefFrame, variable=self.play_bot_ref,
                                       bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                       activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                       relief=FLAT, highlightcolor=self.BACKGROUND)
        play_botrefInput.pack()

        mpFrame = LabelFrame(playVideoFrame, text="Display Meltpool",
                             bd=0, highlightthickness=0, bg=self.BACKGROUND,
                             labelanchor=N, padx=5)
        mpFrame.grid(row=2, column=2, sticky=W + E + N + S)
        play_mpInput = Checkbutton(mpFrame, variable=self.play_disp_mp,
                                   bg=self.BACKGROUND, bd=0, activebackground=self.BACKGROUND,
                                   activeforeground=self.FRAMEBORDER, selectcolor=self.FRAMEBORDER,
                                   relief=FLAT, highlightcolor=self.BACKGROUND)
        play_mpInput.pack()

    def buildPlotOptionsFrame(self):
        plotOptionsFrame = LabelFrame(self.optionsPanel, text="Plot options",
                                      bd=1, highlightthickness=1, highlightcolor=self.FRAMEBORDER,
                                      highlightbackground=self.FRAMEBORDER, bg=self.BACKGROUND,
                                      padx=5, relief=FLAT)
        plotOptionsFrame.grid(row=3, column=0, columnspan=2, sticky=W+E+N+S)

        plotOptionsFrame.columnconfigure(0, weight=1)
        plotOptionsFrame.columnconfigure(1, weight=1)
        plotOptionsFrame.columnconfigure(2, weight=1)
        plotOptionsFrame.rowconfigure(0, weight=1)
        plotOptionsFrame.rowconfigure(1, weight=1)
        plotOptionsFrame.rowconfigure(2, weight=1)

        pixelLocationFrame = LabelFrame(plotOptionsFrame, text="Pixel Location",
                                        bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                        labelanchor=N, padx=5, pady=10)
        pixelLocationFrame.grid(row=0, column=1, sticky=W+E+N+S)

        pixelLocationFrame.columnconfigure(0, weight=1)
        pixelLocationFrame.columnconfigure(1, weight=1)
        pixelLocationFrame.columnconfigure(2, weight=1)
        pixelLocationFrame.rowconfigure(0, weight=1)

        pixelXLocationInput = Entry(pixelLocationFrame, width=4, justify=CENTER, relief=FLAT)
        pixelXLocationInput.grid(row=0, column=0, sticky=W+E+N+S)
        comma = Label(pixelLocationFrame, text=",",
                      bd=0, highlightthickness=0, bg=self.BACKGROUND)
        comma.grid(row=0, column=1, sticky=W+E+N+S)
        pixelYLocationInput = Entry(pixelLocationFrame, width=4, justify=CENTER, relief=FLAT)
        pixelYLocationInput.grid(row=0, column=2, sticky=W + E + N + S)

        histthreshFrame = LabelFrame(plotOptionsFrame, text="Temperature Threshold (histogram)",
                                     bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                     labelanchor=N, padx=5)
        histthreshFrame.grid(row=1, column=0, sticky=W+E+N+S)
        histthreshInput = Entry(histthreshFrame, width=4, justify=CENTER, relief=FLAT)
        histthreshInput.insert(END, 200)
        histthreshInput.pack()

        histBinFrame = LabelFrame(plotOptionsFrame, text="Bin Count (histogram)",
                                  bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                  labelanchor=N, padx=5)
        histBinFrame.grid(row=1, column=1, sticky=W+E+N+S)
        histBinInput = Entry(histBinFrame, width=3, justify=CENTER, relief=FLAT)
        histBinInput.insert(END, 5)
        histBinInput.pack()

        histGradSpacingFrame = LabelFrame(plotOptionsFrame, text="Gradient Spacing (histogram)",
                                          bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                          labelanchor=N, padx=5)
        histGradSpacingFrame.grid(row=1, column=2, sticky=W+E+N+S)
        histGradSpacingInput = Entry(histGradSpacingFrame, width=3, justify=CENTER, relief=FLAT)
        histGradSpacingInput.insert(END, 1)
        histGradSpacingInput.pack()

        frameRangeFrame = LabelFrame(plotOptionsFrame, text="Frame Range (line plot)",
                                     bd=0, highlightthickness=0, bg=self.BACKGROUND,
                                     labelanchor=N, padx=5)
        frameRangeFrame.grid(row=2, column=1, sticky=W+E+N+S)

        frameRangeFrame.columnconfigure(0, weight=1)
        frameRangeFrame.columnconfigure(1, weight=1)
        frameRangeFrame.rowconfigure(0, weight=1)

        plotStartFrameInput = Entry(frameRangeFrame, width=5, justify=CENTER, relief=FLAT)
        plotStartFrameInput.insert(END, 0)
        plotStartFrameInput.grid(row=0, column=0)

        plotEndFrameInput = Entry(frameRangeFrame, width=5, justify=CENTER, relief=FLAT)
        plotEndFrameInput.insert(END, -1)
        plotEndFrameInput.grid(row=0, column=1)

    def buildButtonFrame(self):
        closeButton = Button(self.buttonPanel, text="Close", command=self.root.quit,
                             bg=self.BUTTONBACKGROUND, relief=FLAT)
        closeButton.pack(side=LEFT)

        submitButton = Button(self.buttonPanel, text="Submit", command=lambda: handler.submit(self=self),
                              bg=self.BUTTONBACKGROUND, relief=FLAT)
        submitButton.pack(side=RIGHT)



