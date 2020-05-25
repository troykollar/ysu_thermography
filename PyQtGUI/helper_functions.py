from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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

    checkbutton = QCheckBox()
    checkbutton.setObjectName(name)
    layout.addWidget(checkbutton, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout


def createEntry(text, name, default, size=3):
    layout = QVBoxLayout()

    label = QLabel()
    label.setText(text)
    layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)

    Entry = QLineEdit()
    Entry.setObjectName(name)
    Entry.setAlignment(Qt.AlignCenter)
    Entry.setText(str(default))
    layout.addWidget(Entry, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout

def createRadioGroup(text, dataset):
    groupBox = QGroupBox(text)

    radio1 = QRadioButton(dataset[0])
    radio2 = QRadioButton(dataset[1])
    radio3 = QRadioButton(dataset[2])

    radio3.setChecked(True)

    vbox = QVBoxLayout()
    vbox.addWidget(radio1)
    vbox.addWidget(radio2)
    vbox.addWidget(radio3)
    vbox.addStretch(1)
    groupBox.setLayout(vbox)

    return groupBox


def play():
    pass


def save():
    pass


def saveFrames():
    pass

def genThresh():
    pass