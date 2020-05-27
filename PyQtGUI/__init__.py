from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette

from PyQtGUI.file_path import FileFrame
from PyQtGUI.gui_helper_functions import FileBrowser, createCheckButton, createEntry, createRadioGroup, play, save, \
    saveFrames, genThresh, createRangeEntry, selectPixels, createPlots
from PyQtGUI.palette import MainPalette


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        palette = MainPalette()

        self.remove_top_reflection = QCheckBox()
        self.remove_bot_reflection = QCheckBox()
        self.scale_factor = QLineEdit()
        self.start_frame = QLineEdit()
        self.end_frame = QLineEdit()

        self.contour_threshold = QLineEdit()
        self.frame_focus = None
        self.focus_contour = QRadioButton()
        self.focus_max_temp = QRadioButton()
        self.focus_none = QRadioButton()
        self.focused_frame_size = QLineEdit()
        self.info_pane = None
        self.disp_contour = QRadioButton()
        self.disp_meltpool = QRadioButton()
        self.disp_none = QRadioButton()
        self.fps = QLineEdit()
        self.frame_delay = QLineEdit()

        self.comp_temp_thresh = QLineEdit()

        self.pixelx = QLineEdit()
        self.pixely = QLineEdit()

        self.start_frame_plot = QLineEdit()
        self.end_frame_plot = QLineEdit()

        self.plot_angle = QCheckBox()
        self.plot_mag = QCheckBox()
        self.plot_scatter = QCheckBox()
        self.plot_hex_bin = QCheckBox()
        self.plot_2d_hist = QCheckBox()
        self.plot_3d_bubble = QCheckBox()
        self.all = QCheckBox()

        self.setWindowTitle('YSU Thermography')

        layout = QVBoxLayout()

        FileFrame = self.createFileFrame()
        DataSetOptionsFrame = self.buildDataSetFrame()
        viewerOptionsFrame = self.buildViewerOptions()
        compositeOptions = self.buildCompositeOptions()
        plotOptions = self.buildPlotOptions()
        plotSelect = self.buildPlotSelection()
        ProgressBar = self.buildProgressBar()

        layout.addLayout(FileFrame)
        layout.addWidget(DataSetOptionsFrame)
        layout.addWidget(viewerOptionsFrame)
        layout.addWidget(compositeOptions)
        layout.addWidget(plotOptions)
        layout.addWidget(plotSelect)
        layout.addWidget(ProgressBar)

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

        frame_focus = createRadioGroup("Frame Focus", ['Contour', 'Max Temp', 'None'], [self.focus_contour, self.focus_max_temp, self.focus_none])
        layout.addWidget(frame_focus, alignment=Qt.AlignCenter | Qt.AlignTop)

        focused_frame_size = createEntry("Focused Frame Size", self.focused_frame_size, 20)
        layout.addLayout(focused_frame_size)

        info_pane = createRadioGroup("Info Pane", ['Contour', 'Meltpool', 'None'], [self.disp_contour, self.disp_meltpool, self.disp_none])
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
        PlayVid.clicked.connect(play(self))
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

    def buildPlotSelection(self):
        frame = QGroupBox()
        frame.setAlignment(Qt.AlignCenter)
        frame.setTitle("Gradient Plots")
        frame.setToolTip("Panel to Select Which Gradient Representations to Plot")
        frame.setAutoFillBackground(True)

        layout = QGridLayout()

        plotAngle = createCheckButton("Plot Angle", self.plot_angle)
        layout.addLayout(plotAngle, 0, 0)

        plotMagnitude = createCheckButton("Plot Magnitude", self.plot_mag)
        layout.addLayout(plotMagnitude, 0, 1)

        plotScatter = createCheckButton("Plot Scatter", self.plot_scatter)
        layout.addLayout(plotScatter, 0, 2)

        plotHexBin = createCheckButton("Plot Hex Bin", self.plot_hex_bin)
        layout.addLayout(plotHexBin, 1, 0)

        plot2dHist = createCheckButton("Plot 2D Hist", self.plot_2d_hist)
        layout.addLayout(plot2dHist, 1, 1)

        plot3DBub = createCheckButton("Plot 3D Bubble", self.plot_3d_bubble)
        layout.addLayout(plot3DBub, 1, 2)

        plotAll = createCheckButton("Plot All", self.all)
        layout.addLayout(plotAll, 2, 1)

        frame.setLayout(layout)

        return frame

    def buildProgressBar(self):
        frame = QGroupBox()

        layout = QHBoxLayout()

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        frame.setLayout(layout)

        return frame

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
