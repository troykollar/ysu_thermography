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


# Create GUI
root = Tk()
root.title("YSU Thermography")
# root.iconbitmap("images/YSU_Logo")

# Creating Frame Sections
filePanel = Frame(root).pack(side=TOP, fill=X)
optionsPanel = Frame(root).pack(fill=X)
buttonPanel = Frame(root).pack(side=BOTTOM, fill=X)

# Creating frame to select functions
functionsFrame = LabelFrame(optionsPanel, text="Functions").pack(fill=X)

# Creating Frames to store options for each function
generateImgFrame = LabelFrame(optionsPanel, text="Generate image Options").pack(fill=X)
saveFrameFrame = LabelFrame(optionsPanel, text="Save Frame Options").pack(fill=X)
playVideoFrame = LabelFrame(optionsPanel, text="Play Video Options").pack(fill=X)
saveVideoFrame = LabelFrame(optionsPanel, text="Save Video Options").pack(fill=X)
genThresholdImgFrame = LabelFrame(optionsPanel, text="Threshold Image Options").pack(fill=X)
dataSetFrame = LabelFrame(optionsPanel, text="Dataset Options").pack(fill=X)

# General Function buttons
submit_button = Button(buttonPanel, text="Submit", command=submit).pack(fill=X)
close_button = Button(buttonPanel, text="close", command=root.quit).pack(fill=X)

# Creating variables for checkboxes to change
generateImg = BooleanVar()
saveFrame = BooleanVar()
playVideo = BooleanVar()
saveVideo = BooleanVar()
genThresholdImg = BooleanVar()
dataSet = BooleanVar()

# Placing function checkboxes in function selection frame
generateImgCheckbox = Checkbutton(functionsFrame, variable=generateImg).pack(side=LEFT)
saveFrameCheckbox = Checkbutton(functionsFrame, variable=saveFrame).pack(side=LEFT)
playVideoCheckbox = Checkbutton(functionsFrame, variable=playVideo).pack(side=LEFT)
saveVideoCheckbox = Checkbutton(functionsFrame, variable=saveVideo).pack(side=LEFT)
genThresholdImgCheckbox = Checkbutton(functionsFrame, variable=genThresholdImg).pack(side=LEFT)
dataSetCheckbox = Checkbutton(functionsFrame, variable=dataSet).pack(side=LEFT)

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
