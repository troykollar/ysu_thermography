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


#Create GUI and frames to sort options
optionPanel = Tk()

generateImgFrame = LabelFrame(optionPanel, text="Generate image Options")
saveFrameFrame = LabelFrame(optionPanel, text="Save Frame Options")
playVideoFrame = LabelFrame(optionPanel, text="Play Video Options")
saveVideoFrame = LabelFrame(optionPanel, text ="Save Video Options")
genThresholdImgFrame = LabelFrame(optionPanel, text="Threshold Image Options")



optionPanel.title("YSU Thermography")
#optionPanel.iconbitmap("images/YSU_Logo")

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

submit_button = Button(optionPanel, text="Submit", command=submit)

close_button = Button(optionPanel, text="close", command=optionPanel.quit)

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

submit_button.grid(row=5, column=5)
close_button.grid(row=6, column=6)

optionPanel.mainloop()



