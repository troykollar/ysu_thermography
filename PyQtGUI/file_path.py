
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQtGUI.helper_functions import FileBrowser


class FileFrame(QWidget):

    def __init__(self, Form, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = QWidget(Form)
        self.widget.setGeometry(QRect(40, 150, 600, 27))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QLabel(self.widget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setMinimumSize(QSize(0, 0))
        self.pushButton.setToolTip("Browse For Files Using a Graphical Interface")
        self.pushButton.setAutoFillBackground(True)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("Browse Button")
        self.pushButton.animateClick(2)
        self.pushButton.clicked.connect(self.on_click)
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "File Frame"))
        self.label.setText(_translate("Form", "Path to Data Directory"))
        self.pushButton.setText(_translate("Form", "Browse"))

    def on_click(self):
        FileBrowser()


