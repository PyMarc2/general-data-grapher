from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from gui.mainGrapherViewUi import Ui_grapherWidget


class MainGrapher(QWidget, Ui_grapherWidget):
    def __init__(self):
        super(MainGrapher, self).__init__()
        self.setupUi(self)
