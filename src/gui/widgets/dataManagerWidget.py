from PyQt5.QtWidgets import QWidget
import os
from PyQt5 import uic
dataManagerWidgetPath = os.path.dirname(os.path.realpath(__file__)) + '\\dataManagerWidgetUi.ui'
Ui_dataManagerWidget, QtBaseClass = uic.loadUiType(dataManagerWidgetPath)


class DataManagerWidget(QWidget, Ui_dataManagerWidget):
    def __init__(self):
        super(DataManagerWidget, self).__init__()
        self.setupUi(self)

