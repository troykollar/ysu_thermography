from PyQt5.QtWidgets import *

from PyQtGUI.file_path import FileFrame
from PyQtGUI.palette import MainPalette


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        palette = MainPalette()

        self.setWindowTitle('YSU Thermography')

        layout = QVBoxLayout()

        layout.addWidget(FileFrame(self))

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
