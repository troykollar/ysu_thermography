from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor

from PyQtGUI.file_path import FileFrame
from PyQtGUI.helper_functions import FileBrowser, createCheckButton, createEntry, createRadioGroup, play, save, \
    saveFrames, genThresh, createRangeEntry, selectPixels, createPlots
from PyQtGUI.palette import MainPalette


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        palette = MainPalette()

        self.remove_top_reflection = "TopReflectBool"
        self.remove_bot_reflection = "BotReflectBool"
        self.scale_factor = "ScaleFactorEntry"
        self.start_frame = "StartFrameEntry"
        self.end_frame = "EndFrameEntry"

        self.contour_threshold = "ContourThresh"
        self.frame_focus = "FrameFocus"
        self.focused_frame_size = "FocusFrameSize"
        self.info_pane = "Info Pane"
        self.fps = "fps"
        self.frame_delay = "FrameDelay"

        self.comp_temp_thresh = "CompTempThresh"

        self.pixelx = "pixelx"
        self.pixely = "pixely"

        self.start_frame_plot = "PlotFrameStart"
        self.end_frame_plot = "PlotFrameEnd"

        self.setWindowTitle('YSU Thermography')

        layout = QVBoxLayout()

        FileFrame = self.createFileFrame()
        DataSetOptionsFrame = self.buildDataSetFrame()
        viewerOptionsFrame = self.buildViewerOptions()
        compositeOptions = self.buildCompositeOptions()
        plotOptions = self.buildPlotOptions()

        layout.addLayout(FileFrame)
        layout.addWidget(DataSetOptionsFrame)
        layout.addWidget(viewerOptionsFrame)
        layout.addWidget(compositeOptions)
        layout.addWidget(plotOptions)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setPalette(palette)

    def createFileFrame(self):
        layout = QHBoxLayout()

        label = QLabel()
        label.setText("Path to File Directory: ")
        layout.addWidget(label)

        self.FilelineEdit = QLineEdit()
        layout.addWidget(self.FilelineEdit)

        BrowseButton = QPushButton()
        BrowseButton.setText('Browse')
        BrowseButton.setToolTip("Browse For Files Using a Graphical Interface")
        BrowseButton.setAutoFillBackground(True)
        BrowseButton.setFlat(True)
        BrowseButton.animateClick(2)
        BrowseButton.clicked.connect(self.BrowseFile)
        layout.addWidget(BrowseButton)

        return layout

    def BrowseFile(self):
        BROWSER = FileBrowser()
        self.FilelineEdit.setText(BROWSER.getDirectory())

    def buildDataSetFrame(self):
        frame = QGroupBox()
        frame.setAlignment(Qt.AlignCenter)
        frame.setTitle("Dataset Options")
        frame.setToolTip("Panel to select build options")
        frame.autoFillBackground()
        frame.setBackgroundRole(QPalette.AlternateBase)

        layout = QHBoxLayout()

        top_reflection = createCheckButton('Remove Top Reflection', self.remove_top_reflection)
        layout.addLayout(top_reflection)

        bot_reflection = createCheckButton('Remove Bottom Reflection', self.remove_bot_reflection)
        layout.addLayout(bot_reflection)

        scale_factor = createEntry("Scale Factor", self.scale_factor, 1)
        layout.addLayout(scale_factor)

        start_frame = createEntry("Start Frame", self.start_frame, -1)
        layout.addLayout(start_frame)

        end_frame = createEntry("End Frame", self.end_frame, -1)
        layout.addLayout(end_frame)

        frame.setLayout(layout)

        return frame

    def buildViewerOptions(self):
        frame = QGroupBox()
        frame.setAlignment(Qt.AlignCenter)
        frame.setTitle("Viewer Options")
        frame.setToolTip("Panel to Select Options for Playing or Saving a Build Video")
        frame.autoFillBackground()
        frame.setBackgroundRole(QPalette.AlternateBase)

        layout = QHBoxLayout()

        contour_thresh = createEntry("Contour Threshold", self.contour_threshold, 0)
        layout.addLayout(contour_thresh)

        frame_focus = createRadioGroup("Frame Focus", ['Contour', 'Max Temp', 'None'])
        layout.addWidget(frame_focus, alignment=Qt.AlignCenter | Qt.AlignTop)

        focused_frame_size = createEntry("Focused Frame Size", self.focused_frame_size, 20)
        layout.addLayout(focused_frame_size)

        info_pane = createRadioGroup("Info Pane", ['Contour', 'Meltpool', 'None'])
        layout.addWidget(info_pane, alignment=Qt.AlignCenter | Qt.AlignTop)

        frame_delay = createEntry("Frame Delay (For Play)", self.frame_delay, 1)
        layout.addLayout(frame_delay)

        fps = createEntry("FPS (For Save)", self.fps, 60)
        layout.addLayout(fps)

        buttonLayout = QVBoxLayout()

        PlayVid = QPushButton()
        PlayVid.setText('Play Build')
        PlayVid.setAutoFillBackground(True)
        PlayVid.setFlat(True)
        PlayVid.animateClick(2)
        PlayVid.clicked.connect(play)
        buttonLayout.addWidget(PlayVid, alignment=Qt.AlignCenter | Qt.AlignTop)

        SaveVid = QPushButton()
        SaveVid.setText('Save Build')
        SaveVid.setAutoFillBackground(True)
        SaveVid.setFlat(True)
        SaveVid.animateClick(2)
        SaveVid.clicked.connect(save)
        buttonLayout.addWidget(SaveVid, alignment=Qt.AlignCenter | Qt.AlignTop)

        SaveFrames = QPushButton()
        SaveFrames.setText('Save Frames')
        SaveFrames.setAutoFillBackground(True)
        SaveFrames.setFlat(True)
        SaveFrames.animateClick(2)
        SaveFrames.clicked.connect(saveFrames)
        buttonLayout.addWidget(SaveFrames, alignment=Qt.AlignCenter | Qt.AlignTop)

        layout.addLayout(buttonLayout)

        frame.setLayout(layout)

        return frame

    def buildCompositeOptions(self):
        frame = QGroupBox()
        frame.setAlignment(Qt.AlignCenter)
        frame.setTitle("Composite Options")
        frame.setToolTip("Panel to Select Composite Image Options")
        frame.autoFillBackground()
        frame.setBackgroundRole(QPalette.AlternateBase)

        layout = QHBoxLayout()

        temp_thresh = createEntry("Temperature Threshold", self.comp_temp_thresh, 200)
        layout.addLayout(temp_thresh)

        gen_thresh = QPushButton()
        gen_thresh.setText('Generate Threshold Image')
        gen_thresh.setAutoFillBackground(True)
        gen_thresh.setFlat(True)
        gen_thresh.animateClick(2)
        gen_thresh.clicked.connect(genThresh)
        layout.addWidget(gen_thresh)

        frame.setLayout(layout)

        return frame

    def buildPlotOptions(self):
        frame = QGroupBox()
        frame.setAlignment(Qt.AlignCenter)
        frame.setTitle("Plot Options")
        frame.setToolTip("Panel to Select Plot Options")
        frame.autoFillBackground()
        frame.setBackgroundRole(QPalette.AlternateBase)

        layout = QHBoxLayout()

        temp_thresh = createEntry("Temperature Threshold", self.comp_temp_thresh, 200)
        layout.addLayout(temp_thresh)

        entries = createRangeEntry('Pixel Location', [self.pixelx, self.pixely], ['',''], 'Select Pixels', selectPixels)

        layout.addLayout(entries)

        framerange = createRangeEntry('Frame Range', [self.start_frame_plot, self.end_frame_plot], [str(0), str(-1)],
                                      'Create Plots', createPlots)

        layout.addLayout(framerange)

        frame.setLayout(layout)

        return frame


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
