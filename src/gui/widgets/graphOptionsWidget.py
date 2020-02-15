from PyQt5.QtWidgets import QWidget
import os
from PyQt5 import uic
graphOptionsWidgetPath = os.path.dirname(os.path.realpath(__file__)) + '\\graphOptionsWidgetUi.ui'
Ui_graphOptionsWidget, QtBaseClass = uic.loadUiType(graphOptionsWidgetPath)


class GraphOptionsWidget(QWidget, Ui_graphOptionsWidget):
    def __init__(self):
        super(GraphOptionsWidget, self).__init__()
        self.setupUi(self)