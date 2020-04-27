def getHintTextFileFrame(frame):
    FILEPANEL = {
        'tempDataLabel': "The directory where the thermal data is stored"
    }
    return FILEPANEL.get(frame, " ")

def getHintTextFunctionFrame(frame):
    FUNCTIONPANEL = {
        'genThresholdImgLabel': "Generate an image displaying how often each pixel surpassed a certain temperature "
                                "threshold",
        'saveFrameLabel': "Save a particular frame in 16 bit color",
        'playVideoLabel': "Play the given build as a video",
        'saveVideoLabel': "Save the given build as a video",
        'gradientHistogramLabel': "Display the gradient values of a given pixel in the form of a histogram",
        'pixelTempRangeLabel': "Displays a line chart for a given pixels thermal history"
    }
    return FUNCTIONPANEL.get(frame, " ")

def getHintTextThresholdFrame(frame):
    THRESHOLDFRAME = {
        'thresholdFrame': "Minimum Temperature to be tracked"
    }
    return THRESHOLDFRAME.get(frame, " ")

def getHintTextSaveImageFrame(frame):
    SAVEIMAGEFRAME = {
        'frameFrame': "Frame number within the build to be saved",
        'destDataLabel': "The image number used to identify the image in your files"
    }
    return SAVEIMAGEFRAME.get(frame, " ")

def getHintTextSavePlayFrame(frame):
    SAVEPLAYFRAME = {
        'scaleFactorFrame': "How much to scale or zoom the video by",
        'frameDelayFrame': "How much delay (in ms) between frames when displaying the video",
        'fmaxFrame': "How many pixels around the max temp to highlight",
        'cthreshFrame': "Minimum temperature to be considered part of the contour",
        'fcontourFrame': "How large (in pixels) the contour should be tracked to",
        'fpsFrame': "The framerate (in frames per second) that the saved video should have",
        'toprefFrame': "Check to remove the top reflection in the video",
        'botrefFrame': "Check to remove the bottom reflection in the video",
        'mpFrame': "Check to display the meltpool data on the video",
        'frameRangeFrame': "The frame range to be saved as a video. (-1 as the end frame represents the end)",
        'contourOnImgFrame': "Display the contour data on the video"
    }
    return SAVEPLAYFRAME.get(frame, " ")

def getHintTextPlotOptions(frame):
    PLOTOPTIONSFRAME = {
        'pixelLocationFrame': "The pixel to be tracked (cartesian coordinates)",
        'histthreshFrame': "The minimum temperature the pixel must achieve to track the gradient",
        'histBinFrame': "The amount of bins to be used for the histogram",
        'histGradSpacingFrame': "The spacing to be used when finding the gradient",
        'frameRangeFrame': "The frame range that the thermal history should be plotted for (-1 as the end frame "
                           "represents the end)"
    }
    return PLOTOPTIONSFRAME.get(frame, " ")
