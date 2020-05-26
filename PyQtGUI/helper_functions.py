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
    groupBox.setAutoFillBackground(True),
    groupBox.set

    radio1 = QRadioButton(dataset[0])
    radio2 = QRadioButton(dataset[1])
    radio3 = QRadioButton(dataset[2])

    radio3.setChecked(True)

    vbox = QVBoxLayout()
    vbox.addWidget(radio1, alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addWidget(radio2, alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addWidget(radio3, alignment=Qt.AlignCenter | Qt.AlignTop)
    vbox.addStretch(1)
    groupBox.setLayout(vbox)

    return groupBox

def createRangeEntry(text, names, defaults, buttonText, function):
    layout = QVBoxLayout()

    label = QLabel()
    label.setText(text)
    layout.addWidget(label, alignment=Qt.AlignCenter | Qt.AlignTop)

    entrylayout = QHBoxLayout()

    Entry0 = QLineEdit()
    Entry0.setObjectName(names[0])
    Entry0.setText(defaults[0])
    Entry0.setAlignment(Qt.AlignCenter)
    entrylayout.addWidget(Entry0, alignment=Qt.AlignCenter | Qt.AlignTop)

    Entry1 = QLineEdit()
    Entry1.setObjectName(names[1])
    Entry1.setText(defaults[1])
    Entry1.setAlignment(Qt.AlignCenter)
    entrylayout.addWidget(Entry1, alignment=Qt.AlignCenter | Qt.AlignTop)

    layout.addLayout(entrylayout)

    button = QPushButton()
    button.setText(buttonText)
    button.setAutoFillBackground(True)
    button.setFlat(True)
    button.animateClick(2)
    button.clicked.connect(function)
    layout.addWidget(button, alignment=Qt.AlignCenter | Qt.AlignTop)

    return layout



def play():
    pass

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
