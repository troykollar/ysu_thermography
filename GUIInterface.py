import np_vid_viewer
from tkinter import *
from tkinter import filedialog
import np_vid_viewer.dataset as dset
from np_vid_viewer import NpVidTool
from np_vid_viewer.composite import generate_threshold_image
import graphing



def submit():

    if genThresholdImg.get():
        generate_threshold_image(tempDataEntry.get() + "/thermal_cam_temps.npy", int(genthreshold_thresholdInput.get()))

    if playVideo.get():
        VIEWER = NpVidTool(data_directory=tempDataEntry.get(),
                           r_top_refl=int(play_top_ref.get()),
                           r_bot_refl=int(play_bot_ref.get()),
                           mp_data_on_vid=int(play_disp_mp.get()),
                           follow_max_temp=int(play_fmaxInput.get()),
                           contour_threshold=int(play_cthreshInput.get()),
                           follow_contour=int(play_fcontourInput.get()),
                           contour_data_on_img=int(False))

        VIEWER.play_video(scale_factor=int(play_scaleFactorInput.get()),
                          frame_delay=int(play_frameDelayInput.get()))

    if saveVideo.get():
        VIEWER = NpVidTool(data_directory=tempDataEntry.get(),
                           r_top_refl=int(play_top_ref.get()),
                           r_bot_refl=int(play_bot_ref.get()),
                           mp_data_on_vid=int(play_disp_mp.get()),
                           follow_max_temp=int(play_fmaxInput.get()),
                           contour_threshold=int(play_cthreshInput.get()),
                           follow_contour=int(play_fcontourInput.get()))

        # TODO: Add start and end frame options
        VIEWER.save_video(scale_factor=int(play_scaleFactorInput.get()),
                          framerate=int(save_fpsInput.get()))

    if saveFrame.get():
        VIEWER = NpVidTool(data_directory=tempDataEntry.get())
        VIEWER.save_frame16(int(frameInput.get()), destDataEntry.get())

    if gradientHistogram.get():
        graphing.plotHistogram(temp_file=tempDataEntry.get() + "/thermal_cam_temps.npy",
                               pixel=(int(pixelXLocationInput.get()), int(pixelYLocationInput.get())),
                               threshold=int(histthreshInput.get()),
                               binCount=int(histBinInput.get()),
                               spacing=int(histGradSpacingInput.get()))

    if pixelTempRange.get():
        graphing.plotLine(temp_file=tempDataEntry.get() + "/thermal_cam_temps.npy",
                          pixel=(int(pixelXLocationInput.get()), int(pixelYLocationInput.get())),
                          startFrame=int(plotStartFrameInput.get()),
                          endFrame=int(plotEndFrameInput.get()))


def browseFiles(entry):
    entry.delete(0, END)
    root.filepath = filedialog.askdirectory(initialdir="/home/rjyarwood/Documents/Research/ResearchData")
    entry.insert(0, root.filepath)


# Create GUI
root = Tk()
root.title("YSU Thermography")
# root.iconbitmap("images/YSU_Logo")

# Creating Frame Sections
filePanel = Frame(root)
filePanel.pack(side=TOP, fill=X, pady=10)
optionsPanel = Frame(root)
optionsPanel.pack(fill=X)
buttonPanel = Frame(root)
buttonPanel.pack(side=BOTTOM, fill=X)

# Creating Frames to store options for each function
dataSetFrame = LabelFrame(optionsPanel, text="Dataset Options")
dataSetFrame.pack(fill=X)


'''FILE FRAME'''
tempDataLabel = Label(filePanel, text="File Path Build Data Folder: ")
tempDataLabel.pack(side=LEFT)
tempDataEntry = Entry(filePanel, width=100)
tempDataEntry.pack(side=LEFT)

tempDataBrowse = Button(filePanel, text="Browse", command=lambda: browseFiles(tempDataEntry))
tempDataBrowse.pack(side=LEFT)
'''END OF FILE FRAME'''


'''FUNCTION FRAMES'''
functionsFrame = LabelFrame(optionsPanel, text="Functions")
functionsFrame.pack(fill=X, ipady=5, pady=10)

# Creating variables for checkboxes to change
generateImg = BooleanVar()
saveFrame = BooleanVar()
playVideo = BooleanVar()
saveVideo = BooleanVar()
genThresholdImg = BooleanVar()
dataSet = BooleanVar()
gradientHistogram = BooleanVar()
#scatterPlot = BooleanVar()
pixelTempRange = BooleanVar()

# Placing function checkboxes in function selection frame
genThresholdImgLabel = LabelFrame(functionsFrame, text="Gen Threshold Img", bd=0, highlightthickness=0)
genThresholdImgLabel.pack(side=LEFT, expand=1)
genThresholdImgCheckbox = Checkbutton(genThresholdImgLabel, variable=genThresholdImg)
genThresholdImgCheckbox.pack()


saveFrameLabel = LabelFrame(functionsFrame, text="Save Frame", bd=0, highlightthickness=0)
saveFrameLabel.pack(side=LEFT, expand=1)
saveFrameCheckbox = Checkbutton(saveFrameLabel, variable=saveFrame)
saveFrameCheckbox.pack()


playVideoLabel = LabelFrame(functionsFrame, text="Play Video", bd=0, highlightthickness=0)
playVideoLabel.pack(side=LEFT, expand=1)
playVideoCheckbox = Checkbutton(playVideoLabel, variable=playVideo)
playVideoCheckbox.pack()


saveVideoLabel = LabelFrame(functionsFrame, text="Save Video", bd=0, highlightthickness=0)
saveVideoLabel.pack(side=LEFT, expand=1)
saveVideoCheckbox = Checkbutton(saveVideoLabel, variable=saveVideo)
saveVideoCheckbox.pack()

'''
dataSetLabel = LabelFrame(functionsFrame, text="Dataset")
dataSetLabel.pack(side=LEFT, expand=1)
dataSetCheckbox = Checkbutton(dataSetLabel, variable=dataSet)
dataSetCheckbox.pack()
'''

gradientHistogramLabel = LabelFrame(functionsFrame, text="Gradient Histogram", bd=0, highlightthickness=0)
gradientHistogramLabel.pack(side=LEFT, expand=1)
gradientHistogramCheckbox = Checkbutton(gradientHistogramLabel, variable=gradientHistogram)
gradientHistogramCheckbox.pack()

'''
scatterPlotLabel = LabelFrame(functionsFrame, text="Scatter Plot")
scatterPlotLabel.pack(side=LEFT, expand=1)
scatterPlotCheckbox = Checkbutton(scatterPlotLabel, variable=scatterPlot)
scatterPlotCheckbox.pack()
'''

pixelTempRangeLabel = LabelFrame(functionsFrame, text="Pixel Temp Line Plot", bd=0, highlightthickness=0)
pixelTempRangeLabel.pack(side=LEFT, expand=1)
pixelTempRangeCheckbox = Checkbutton(pixelTempRangeLabel, variable=pixelTempRange)
pixelTempRangeCheckbox.pack()
'''END OF FUNCTION FRAME'''


'''GENERATE THRESHOLD IMAGE FRAME'''
genThresholdImgFrame = LabelFrame(optionsPanel, text="Threshold Image Options")
genThresholdImgFrame.pack(fill=X)

thresholdFrame = LabelFrame(genThresholdImgFrame, text="Temperature Threshold")
thresholdFrame.pack(side=LEFT, expand=1)
genthreshold_thresholdInput = Entry(thresholdFrame, width=3)
genthreshold_thresholdInput.pack()
'''END OF GENERATE THRESHOLD IMAGE FRAME'''



'''SAVE IMAGE FRAME'''
saveFrameFrame = LabelFrame(optionsPanel, text="Save Frame Options")
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
'''END OF SAVE IMAGE FRAME'''


'''PLAY VIDEO FRAME'''
play_disp_mp = BooleanVar()
play_top_ref = BooleanVar()
play_bot_ref = BooleanVar()

playVideoFrame = LabelFrame(optionsPanel, text="Play and Save Video Options")
playVideoFrame.pack(fill=X, ipady=10)

scaleFactorFrame = LabelFrame(playVideoFrame, text="Scale Factor", padx=7)
scaleFactorFrame.pack(side=LEFT, expand=1)
play_scaleFactorInput = Entry(scaleFactorFrame, width=2)
play_scaleFactorInput.insert(END, 1)
play_scaleFactorInput.pack()

frameDelayFrame = LabelFrame(playVideoFrame, text="Frame Delay (for play video)", padx=7)
frameDelayFrame.pack(side=LEFT, expand=1)
play_frameDelayInput = Entry(frameDelayFrame, width=2)
play_frameDelayInput.insert(END, 1)
play_frameDelayInput.pack()

fmaxFrame = LabelFrame(playVideoFrame, text="# pixels around max temp", padx=7)
fmaxFrame.pack(side=LEFT, expand=1)
play_fmaxInput = Entry(fmaxFrame, width=3)
play_fmaxInput.insert(END, False)
play_fmaxInput.pack()

cthreshFrame = LabelFrame(playVideoFrame, text="Contour Temp Thresh", padx=7)
cthreshFrame.pack(side=LEFT, expand=1)
play_cthreshInput = Entry(cthreshFrame, width=3)
play_cthreshInput.insert(END, 0)
play_cthreshInput.pack()

fcontourFrame = LabelFrame(playVideoFrame, text="Contour Pixel Range", padx=7)
fcontourFrame.pack(side=LEFT, expand=1)
play_fcontourInput = Entry(fcontourFrame, width=3)
play_fcontourInput.insert(END, False)
play_fcontourInput.pack()

mpFrame = LabelFrame(playVideoFrame, text="Display Meltpool", padx=7)
mpFrame.pack(side=LEFT, expand=1)
play_mpInput = Checkbutton(mpFrame, variable=play_disp_mp)
play_mpInput.pack()

toprefFrame = LabelFrame(playVideoFrame, text="Remove Top Reflection", padx=7)
toprefFrame.pack(side=LEFT, expand=1)
play_toprefInput = Checkbutton(toprefFrame, variable=play_top_ref)
play_toprefInput.pack()

botrefFrame = LabelFrame(playVideoFrame, text="Remove Bottom Reflection", padx=7)
botrefFrame.pack(side=LEFT, expand=1)
play_botrefInput = Checkbutton(botrefFrame, variable=play_bot_ref)
play_botrefInput.pack()

fpsFrame = LabelFrame(playVideoFrame, text="Framerate (For Save Video Only)", padx=7)
fpsFrame.pack(side=LEFT, expand=1)
save_fpsInput = Entry(fpsFrame, width=3)
save_fpsInput.insert(END, 60)
save_fpsInput.pack()
'''END OF PLAY VIDEO FRAME'''

"""
'''SAVE VIDEO FRAME'''
save_disp_mp = BooleanVar()
save_top_ref = BooleanVar()
save_bot_ref = BooleanVar()

saveVideoFrame = LabelFrame(optionsPanel, text="Save Video Options")
saveVideoFrame.pack(fill=X)

scaleFactorFrame = LabelFrame(saveVideoFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
save_scaleFactorInput = Entry(scaleFactorFrame, width=3)
save_scaleFactorInput.insert(END, 1)
save_scaleFactorInput.pack()

frameDelayFrame = LabelFrame(saveVideoFrame, text="Frame Delay")
frameDelayFrame.pack(side=LEFT, expand=1)
save_frameDelayInput = Entry(frameDelayFrame, width=4)
save_frameDelayInput.insert(END, 1)
save_frameDelayInput.pack()

fmaxFrame = LabelFrame(saveVideoFrame, text="# pixels around max temp")
fmaxFrame.pack(side=LEFT, expand=1)
save_fmaxInput = Entry(fmaxFrame, width=3)
save_fmaxInput.insert(END, False)
save_fmaxInput.pack()

cthreshFrame = LabelFrame(saveVideoFrame, text="Contour Temp Thresh")
cthreshFrame.pack(side=LEFT, expand=1)
save_cthreshInput = Entry(cthreshFrame, width=3)
save_cthreshInput.insert(END, 0)
save_cthreshInput.pack()

fcontourFrame = LabelFrame(saveVideoFrame, text="Contour Pixel Range")
fcontourFrame.pack(side=LEFT, expand=1)
save_fcontourInput = Entry(fcontourFrame, width=3)
save_fcontourInput.insert(END, False)
save_fcontourInput.pack()

fpsFrame = LabelFrame(saveVideoFrame, text="Framerate")
fpsFrame.pack(side=LEFT, expand=1)
save_fpsInput = Entry(fpsFrame, width=3)
save_fpsInput.insert(END, 60)
save_fpsInput.pack()

mpFrame = LabelFrame(saveVideoFrame, text="Display Meltpool")
mpFrame.pack(side=LEFT, expand=1)
save_mpInput = Checkbutton(mpFrame, variable=save_disp_mp)
save_mpInput.pack()

toprefFrame = LabelFrame(saveVideoFrame, text="Remove Top Reflection")
toprefFrame.pack(side=LEFT, expand=1)
save_toprefInput = Checkbutton(toprefFrame, variable=save_top_ref)
save_toprefInput.pack()

botrefFrame = LabelFrame(saveVideoFrame, text="Remove Bottom Reflection")
botrefFrame.pack(side=LEFT, expand=1)
save_botrefInput = Checkbutton(botrefFrame, variable=save_bot_ref)
save_botrefInput.pack()
'''END OF SAVE VIDEO FRAME'''"""


'''DATASET FRAME'''
functionsFrame = LabelFrame(optionsPanel, text="Functions")
functionsFrame.pack(fill=X)
'''END OF DATASET FRAME'''

'''HISTOGRAM FRAME'''
plotOptionsFrame = LabelFrame(optionsPanel, text="Plot options")
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
'''END OF HISTOGRAM FRAME'''

'''BUTTON FRAME'''
closeButton = Button(buttonPanel, text="Close", command=root.quit)
closeButton.pack(side=LEFT)

submitButton = Button(buttonPanel, text="Submit", command=submit)
submitButton.pack(side=RIGHT)
'''END OF BUTTON FRAME'''


root.mainloop()
