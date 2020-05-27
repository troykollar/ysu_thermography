from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dataset import DataSet
from viewer import Viewer


class Validator(QValidator):

    def __init__(self):
        super().__init__()

class FileBrowser(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'File Browser'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

    def getDirectory(self):
        return str(self.fileName)


def createCheckButton(text, name):
    layout = QVBoxLayout()

    label = QLabel()
    label.setText(text)
    layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)

    layout.addWidget(name, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout


def createEntry(text, name, default, size=3):
    layout = QVBoxLayout()

    label = QLabel()
    label.setText(text)
    layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)

    name.setAlignment(Qt.AlignCenter)
    name.setText(str(default))
    layout.addWidget(name, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout

def createRadioGroup(text, dataset, self):
    groupBox = QGroupBox(text)
    groupBox.setAutoFillBackground(True),

    self[0] = QRadioButton(dataset[0])
    self[1] = QRadioButton(dataset[1])
    self[2] = QRadioButton(dataset[2])

    self[2].setChecked(True)

    vbox = QVBoxLayout()
    vbox.addWidget(self[0], alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addWidget(self[1], alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addWidget(self[2], alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addStretch(1)
    groupBox.setLayout(vbox)

    return groupBox

def createRangeEntry(text, names, defaults, buttonText, function):
    layout = QVBoxLayout()

    label = QLabel()
    label.setText(text)
    layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)

    entrylayout = QHBoxLayout()

    names[0] = QLineEdit()
    names[0].setText(defaults[0])
    names[0].setAlignment(Qt.AlignCenter)
    entrylayout.addWidget(names[0], alignment=Qt.AlignCenter | Qt.AlignTop)

    names[1] = QLineEdit()
    names[1].setText(defaults[1])
    names[1].setAlignment(Qt.AlignCenter)
    entrylayout.addWidget(names[1], alignment=Qt.AlignCenter | Qt.AlignTop)

    layout.addLayout(entrylayout)

    button = QPushButton()
    button.setText(buttonText)
    button.setAutoFillBackground(True)
    button.setFlat(True)
    button.animateClick(2)
    button.clicked.connect(function)
    layout.addWidget(button, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout


def grab_dataset(self):
    self.dataset = DataSet(self.FilelineEdit.text() + '/thermal_cam_temps.npy',
                           self.FilelineEdit.text()+
                           '/merged_data.npy' if self.disp_meltpool else None,
                           remove_top_reflection=self.remove_top_reflection.isChecked(),
                           remove_bottom_reflection=self.remove_bot_reflection.isChecked(),
                           scale_factor=self.scale_factor.text(),
                           start_frame=self.start_frame.text(),
                           end_frame=self.end_frame.text())


def grab_viewer(self):
    if self.focused_contour.isChecked():
        follow = 'contour'

    elif self.focused.max_temp.isChecked():
        follow = 'max'

    else:
        follow = None

    if self.disp_contour.isChecked():
        info_pane = 'contour'

    elif self.disp_meltpool.isChecked():
        info_pane = 'mp'

    else:
        info_pane = None

    self.viewer = Viewer(self.dataset, self.contour_threshold.text(),
                         follow, self.focused_frame_size.text(),
                         info_pane)


def play(self):
    grab_dataset(self)
    grab_viewer(self)
    self.viewer.play_video(self.frame_delay.get())

def save():
    pass

def saveFrames():
    pass

def genThresh():
    pass

def selectPixels():
    pass

def createPlots():
    pass
