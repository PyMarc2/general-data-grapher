from PyQt5.QtWidgets import QWidget
import pyqtgraph
import os
from PyQt5 import uic


class PyqtGraphWidget(pyqtgraph.GraphicsLayoutWidget):
    def __init__(self):
        super(PyqtGraphWidget, self).__init__()
        self.setBackground('w')
        self.addPlot()


