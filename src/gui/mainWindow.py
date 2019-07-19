from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from gui.mainWindowUi import Ui_MainWindow
from gui.mainGrapherView import MainGrapher


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.mainGrapher = MainGrapher()
        self.setCentralWidget(self.mainGrapher)



