

def getHintTextFunctionFrame(frame):
    FUNCTIONPANEL = {
        'genThresholdImgLabel': "Generate an image displaying how often each pixel surpassed a certain temperature "
                                "threshold",
        'saveFrame': "Save a particular frame in 16 bit color",
        'playVideoLabel': "Play the given build as a video",
        'saveVideoLabel': "Save the given build as a video",
        'gradientHistogram': "Display the gradient values of a given pixel in the form of a histogram",
        'pixelTempRangeLabel': "Displays a line chart for a given pixels thermal history"
    }
    return FUNCTIONPANEL.get(frame, " ")

def getHintTextThresholdFrame(frame):
    THRESHOLDFRAME = {
        'thresholdFrame': "Minimum Temperature to be tracked"
    }
    return THRESHOLDFRAME.get(frame, " ")

