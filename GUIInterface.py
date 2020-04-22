# import   np_vid_viewer

# temp_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/thermal_cam_temps.npy"
# merged_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/merged_data.npy"

import np_vid_viewer
from tkinter import *


def submit():
    VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                     data_filename=merged_data_file,
                                     mp_data_on_vid=False,
                                     remove_top_reflection=False,
                                     remove_bottom_reflection=False)

    VIEWER.play_video()

# To quickly create check buttons with the labels on top


# Create GUI
root = Tk()
root.title("YSU Thermography")
# root.iconbitmap("images/YSU_Logo")

# Creating Frame Sections
filePanel = Frame(root)
filePanel.pack(side=TOP, fill=X)
optionsPanel = Frame(root)
optionsPanel.pack(fill=X)
buttonPanel = Frame(root)
buttonPanel.pack(side=BOTTOM, fill=X)

# Creating Frames to store options for each function


saveVideoFrame = LabelFrame(optionsPanel, text="Save Video Options")
saveVideoFrame.pack(fill=X)

genThresholdImgFrame = LabelFrame(optionsPanel, text="Threshold Image Options")
genThresholdImgFrame.pack(fill=X)

dataSetFrame = LabelFrame(optionsPanel, text="Dataset Options")
dataSetFrame.pack(fill=X)


'''FILE FRAME'''
tempDataLabel = Label(filePanel, text="File Path to Temperature Data:")
tempDataLabel.grid(row=0, column=0)
tempDataEntry = Entry(filePanel)
tempDataEntry.grid(row=0, column=1)

mergedDataLabel = Label(filePanel, text="File Path to Merged Data:")
mergedDataLabel.grid(row=1, column=0)
mergedDataEntry = Entry(filePanel)
mergedDataEntry.grid(row=1, column=1)
'''END OF FILE FRAME'''


'''FUNCTION FRAMES'''
# Creating frame to select functions
functionsFrame = LabelFrame(optionsPanel, text="Functions")
functionsFrame.pack(fill=X)

# Creating variables for checkboxes to change
generateImg = BooleanVar()
saveFrame = BooleanVar()
playVideo = BooleanVar()
saveVideo = BooleanVar()
genThresholdImg = BooleanVar()
dataSet = BooleanVar()

# Placing function checkboxes in function selection frame
generateImgLabel = LabelFrame(functionsFrame, text="Generate Image")
generateImgLabel.pack(side=LEFT, expand=1)
generateImgCheckbox = Checkbutton(generateImgLabel, variable=generateImg)
generateImgCheckbox.pack()


saveFrameLabel = LabelFrame(functionsFrame, text="Save Frame")
saveFrameLabel.pack(side=LEFT, expand=1)
saveFrameCheckbox = Checkbutton(saveFrameLabel, variable=saveFrame)
saveFrameCheckbox.pack()


playVideoLabel = LabelFrame(functionsFrame, text="Play Video")
playVideoLabel.pack(side=LEFT, expand=1)
playVideoCheckbox = Checkbutton(playVideoLabel, variable=playVideo)
playVideoCheckbox.pack()


saveVideoLabel = LabelFrame(functionsFrame, text="Save Video")
saveVideoLabel.pack(side=LEFT, expand=1)
saveVideoCheckbox = Checkbutton(saveVideoLabel, variable=saveVideo)
saveVideoCheckbox.pack()


genThresholdImgLabel = LabelFrame(functionsFrame, text="Gen Threshold Img")
genThresholdImgLabel.pack(side=LEFT, expand=1)
genThresholdImgCheckbox = Checkbutton(genThresholdImgLabel, variable=genThresholdImg)
genThresholdImgCheckbox.pack()


dataSetLabel = LabelFrame(functionsFrame, text="Dataset")
dataSetLabel.pack(side=LEFT, expand=1)
dataSetCheckbox = Checkbutton(dataSetLabel, variable=dataSet)
dataSetCheckbox.pack()
'''END OF FUNCTION FRAME'''


'''GENERATE IMAGE FRAME'''
generateImgFrame = LabelFrame(optionsPanel, text="Generate image Options")
generateImgFrame.pack(fill=X)

frameNumberFrame = LabelFrame(generateImgFrame, text="Frame Number")
frameNumberFrame.pack(side=LEFT, expand=1)
frameNumberInput = Entry(frameNumberFrame)
frameNumberInput.pack()

scaleFactorFrame = LabelFrame(generateImgFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
scaleFactorInput = Entry(scaleFactorFrame)
scaleFactorInput.pack()
'''END OF GENERATE IMAGE FRAME'''


'''SAVE IMAGE FRAME'''
saveFrameFrame = LabelFrame(optionsPanel, text="Save Frame Options")
saveFrameFrame.pack(fill=X)

startFrameFrame = LabelFrame(saveFrameFrame, text="Start Frame")
startFrameFrame.pack(side=LEFT, expand=1)
startFrameInput = Entry(startFrameFrame)
startFrameInput.pack()

endFrameFrame = LabelFrame(saveFrameFrame, text="End Frame")
endFrameFrame.pack(side=LEFT, expand=1)
endFrameInput = Entry(endFrameFrame)
endFrameInput.pack()

scaleFactorFrame = LabelFrame(saveFrameFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
scaleFactorInput = Entry(scaleFactorFrame)
scaleFactorInput.pack()
'''END OF SAVE IMAGE FRAME'''


'''PLAY VIDEO FRAME'''
playVideoFrame = LabelFrame(optionsPanel, text="Play Video Options")
playVideoFrame.pack(fill=X)

scaleFactorFrame = LabelFrame(playVideoFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
scaleFactorInput = Entry(scaleFactorFrame)
scaleFactorInput.pack()

frameDelayFrame = LabelFrame(playVideoFrame, text="Scale Factor")
frameDelayFrame.pack(side=LEFT, expand=1)
frameDelayInput = Entry(frameDelayFrame)
frameDelayInput.pack()
'''END OF PLAY VIDEO FRAME'''


'''BUTTON FRAME'''
closeButton = Button(buttonPanel, text="Close", command=root.quit)
closeButton.pack(side=LEFT)

submitButton = Button(buttonPanel, text="Submit", command=submit)
submitButton.pack(side=RIGHT)
'''END OF BUTTON FRAME'''




'''
temp_data_label = Label(optionPanel, text="Path to temperature data")
temp_data_file = Entry(optionPanel)

merged_data_label = Label(optionPanel, text="Path to merged data")
merged_data_file = Entry(optionPanel)

mp_data_label = Label(optionPanel, text="meltpool data on vid")
mp_data_on_vid = Checkbutton(optionPanel)

remove_bottom_label = Label(optionPanel, text="Remove bottom reflection")
remove_bottom_reflection = Checkbutton(optionPanel)

remove_top_label = Label(optionPanel, text="Remove top reflection")
remove_top_reflection = Checkbutton(optionPanel)

play_vid_label = Label(optionPanel, text="play video")
play_vid = Checkbutton(optionPanel)



merged_data_label.grid(row=1, column=0)
merged_data_file.grid(row=1, column=1, columnspan=7)

temp_data_label.grid(row=0, column=0)
temp_data_file.grid(row=0, column=1, columnspan=7)

mp_data_label.grid(row=3, column=0)
mp_data_on_vid.grid(row=4, column=0)

remove_bottom_label.grid(row=3, column=1)
remove_bottom_reflection.grid(row=4, column=1)

remove_top_label.grid(row=3, column=2)
remove_top_reflection.grid(row=4, column=2)

play_vid_label.grid(row=5, column=0)
play_vid.grid(row=6, column=0)
'''


root.mainloop()
