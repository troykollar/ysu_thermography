# import   np_vid_viewer

# temp_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/thermal_cam_temps.npy"
# merged_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/merged_data.npy"

import np_vid_viewer
from tkinter import *
from tkinter import filedialog
import np_vid_viewer.dataset as dset
from np_vid_viewer import NpVidTool


def submit():

    if genThresholdImg.get():
        composite.generate_threshold_image(
            tempDataEntry.get() + "/thermal_cam_temps.npy",
            int(genthreshold_thresholdInput.get()))

    if playVideo.get():
        VIEWER = NpVidTool(tempDataEntry.get(),
                           int(play_top_ref.get()),
                           int(play_bot_ref.get()),
                           int(play_disp_mp.get()),
                           int(play_fmaxInput.get()),
                           contour_threshold=int(play_cthreshInput.get()),
                           follow_contour=int(play_fcontourInput.get()),
                           contour_data_on_img=int(False))

        VIEWER.play_video(int(play_scaleFactorInput.get()),
                          int(play_frameDelayInput.get()))

    if saveVideo.get():
        VIEWER = NpVidTool(tempDataEntry.get(),
                           int(save_top_ref.get()),
                           int(save_bot_ref.get()),
                           int(save_disp_mp.get()),
                           follow_max_temp=int(save_fmaxInput.get()),
                           contour_threshold=int(save_cthreshInput.get()),
                           follow_contour=int(save_fcontourInput.get()))

        #TODO: Add start and end frame options
        VIEWER.save_video(int(save_scaleFactorInput.get()),
                          int(save_fpsInput.get()))

    if saveFrame.get():
        VIEWER = np_vid_viewer.NpVidTool(data_directory=tempDataEntry.get())
        VIEWER.save_frame16(int(frameInput.get()), destDataEntry.get())


def browseFiles(entry):
    entry.delete(0, END)
    root.filepath = filedialog.askdirectory(initialdir="~Documents")
    entry.insert(0, root.filepath)


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
dataSetFrame = LabelFrame(optionsPanel, text="Dataset Options")
dataSetFrame.pack(fill=X)
'''FILE FRAME'''
tempDataLabel = Label(filePanel, text="File Path Build Data Folder: ")
tempDataLabel.pack(side=LEFT)
tempDataEntry = Entry(filePanel, width=100)
tempDataEntry.pack(side=LEFT, fill=X)

tempDataBrowse = Button(filePanel,
                        text="Browse",
                        command=lambda: browseFiles(tempDataEntry))
tempDataBrowse.pack(side=LEFT)
'''END OF FILE FRAME'''
'''FUNCTION FRAMES'''
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
genThresholdImgLabel = LabelFrame(functionsFrame, text="Gen Threshold Img")
genThresholdImgLabel.pack(side=LEFT, expand=1)
genThresholdImgCheckbox = Checkbutton(genThresholdImgLabel,
                                      variable=genThresholdImg)
genThresholdImgCheckbox.pack()
'''
saveFrameLabel = LabelFrame(functionsFrame, text="Save Frame")
saveFrameLabel.pack(side=LEFT, expand=1)
saveFrameCheckbox = Checkbutton(saveFrameLabel, variable=saveFrame)
saveFrameCheckbox.pack()
'''

playVideoLabel = LabelFrame(functionsFrame, text="Play Video")
playVideoLabel.pack(side=LEFT, expand=1)
playVideoCheckbox = Checkbutton(playVideoLabel, variable=playVideo)
playVideoCheckbox.pack()

saveVideoLabel = LabelFrame(functionsFrame, text="Save Video")
saveVideoLabel.pack(side=LEFT, expand=1)
saveVideoCheckbox = Checkbutton(saveVideoLabel, variable=saveVideo)
saveVideoCheckbox.pack()
'''
dataSetLabel = LabelFrame(functionsFrame, text="Dataset")
dataSetLabel.pack(side=LEFT, expand=1)
dataSetCheckbox = Checkbutton(dataSetLabel, variable=dataSet)
dataSetCheckbox.pack()
'''
'''END OF FUNCTION FRAME'''
'''GENERATE THRESHOLD IMAGE FRAME'''
genThresholdImgFrame = LabelFrame(optionsPanel, text="Threshold Image Options")
genThresholdImgFrame.pack(fill=X)

thresholdFrame = LabelFrame(genThresholdImgFrame, text="Temperature Threshold")
thresholdFrame.pack(side=LEFT, expand=1)
genthreshold_thresholdInput = Entry(thresholdFrame, width=3)
genthreshold_thresholdInput.pack()
'''END OF GENERATE THRESHOLD IMAGE FRAME'''
"""
'''SAVE IMAGE FRAME'''
saveFrameFrame = LabelFrame(optionsPanel, text="Save Frame Options")
saveFrameFrame.pack(fill=X)

frameFrame = LabelFrame(saveFrameFrame, text="Frame")
frameFrame.pack(side=LEFT, expand=1)
frameInput = Entry(frameFrame)
frameInput.pack()

destDataLabel = Label(saveFrameFrame, text="DestinationPath: ")
destDataLabel.pack(side=LEFT)
destDataEntry = Entry(saveFrameFrame, width=100)
destDataEntry.pack(side=LEFT, fill=X)

destDataBrowse = Button(saveFrameFrame, text="Browse", command=lambda: browseFiles(frameInput))
destDataBrowse.pack(side=LEFT)
'''END OF SAVE IMAGE FRAME'''
"""
'''PLAY VIDEO FRAME'''
play_disp_mp = BooleanVar()
play_top_ref = BooleanVar()
play_bot_ref = BooleanVar()

playVideoFrame = LabelFrame(optionsPanel, text="Play Video Options")
playVideoFrame.pack(fill=X)

scaleFactorFrame = LabelFrame(playVideoFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
play_scaleFactorInput = Entry(scaleFactorFrame, width=2)
play_scaleFactorInput.insert(END, 1)
play_scaleFactorInput.pack()

frameDelayFrame = LabelFrame(playVideoFrame, text="Frame Delay")
frameDelayFrame.pack(side=LEFT, expand=1)
play_frameDelayInput = Entry(frameDelayFrame, width=2)
play_frameDelayInput.insert(END, 1)
play_frameDelayInput.pack()

fmaxFrame = LabelFrame(playVideoFrame, text="# pixels around max temp")
fmaxFrame.pack(side=LEFT, expand=1)
play_fmaxInput = Entry(fmaxFrame, width=3)
play_fmaxInput.insert(END, False)
play_fmaxInput.pack()

cthreshFrame = LabelFrame(playVideoFrame, text="Contour Temp Thresh")
cthreshFrame.pack(side=LEFT, expand=1)
play_cthreshInput = Entry(cthreshFrame, width=3)
play_cthreshInput.insert(END, 0)
play_cthreshInput.pack()

fcontourFrame = LabelFrame(playVideoFrame, text="Contour Pixel Range")
fcontourFrame.pack(side=LEFT, expand=1)
play_fcontourInput = Entry(fcontourFrame, width=3)
play_fcontourInput.insert(END, False)
play_fcontourInput.pack()

mpFrame = LabelFrame(playVideoFrame, text="Display Meltpool")
mpFrame.pack(side=LEFT, expand=1)
play_mpInput = Checkbutton(mpFrame, variable=play_disp_mp)
play_mpInput.pack()

toprefFrame = LabelFrame(playVideoFrame, text="Remove Top Reflection")
toprefFrame.pack(side=LEFT, expand=1)
play_toprefInput = Checkbutton(toprefFrame, variable=play_top_ref)
play_toprefInput.pack()

botrefFrame = LabelFrame(playVideoFrame, text="Remove Bottom Reflection")
botrefFrame.pack(side=LEFT, expand=1)
play_botrefInput = Checkbutton(botrefFrame, variable=play_bot_ref)
play_botrefInput.pack()
'''END OF PLAY VIDEO FRAME'''
'''SAVE VIDEO FRAME'''
save_disp_mp = BooleanVar()
save_top_ref = BooleanVar()
save_bot_ref = BooleanVar()

saveVideoFrame = LabelFrame(optionsPanel, text="Save Video Options")
saveVideoFrame.pack(fill=X)

scaleFactorFrame = LabelFrame(saveVideoFrame, text="Scale Factor")
scaleFactorFrame.pack(side=LEFT, expand=1)
save_scaleFactorInput = Entry(scaleFactorFrame, width=2)
save_scaleFactorInput.insert(END, 1)
save_scaleFactorInput.pack()

frameDelayFrame = LabelFrame(saveVideoFrame, text="Frame Delay")
frameDelayFrame.pack(side=LEFT, expand=1)
save_frameDelayInput = Entry(frameDelayFrame, width=2)
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
'''END OF SAVE VIDEO FRAME'''
'''DATASET FRAME'''
functionsFrame = LabelFrame(optionsPanel, text="Functions")
functionsFrame.pack(fill=X)
'''END OF DATASET FRAME'''
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
