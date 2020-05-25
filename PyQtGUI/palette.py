from PyQt5.QtGui import QPalette, QColor
import PyQtGUI.CONSTANTS as const


class MainPalette(QPalette):
    def __init__(self):
        super(MainPalette, self).__init__()

        self.setColor(QPalette.Window, QColor(const.MAINWINDOW))
        self.setColor(QPalette.WindowText, QColor(const.WINDOWTEXT))
        self.setColor(QPalette.Base, QColor(const.BASE))
        self.setColor(QPalette.Button, QColor(const.BUTTON))
        self.setColor(QPalette.ButtonText, QColor(const.BUTTONTEXT))
        self.setColor(QPalette.AlternateBase, QColor(const.ALTERNATEBASE))

class TabPalette(QPalette):
    def __init__(self):
        super(TabPalette, self).__init__()

        self.setColor(QPalette.Window, QColor(const.TABWINDOW))
        self.setColor(QPalette.WindowText, QColor(const.WINDOWTEXT))
        self.setColor(QPalette.Base, QColor(const.BASE))
        self.setColor(QPalette.Button, QColor(const.BUTTON))
        self.setColor(QPalette.ButtonText, QColor(const.BUTTONTEXT))
