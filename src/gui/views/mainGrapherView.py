from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTabWidget, QFrame, QSplitter
from PyQt5.QtCore import pyqtSignal, Qt
from gui.widgets.graphManagerWidget import GraphManagerWidget
from gui.widgets.pyqtGraphWidget import PyqtGraphWidget
import os
from PyQt5 import uic


class WorkspaceManagerView(QWidget):
    def __init__(self):
        super(WorkspaceManagerView, self).__init__()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        mainTabWidget = QTabWidget()

        graphOptionsWidget = GraphManagerWidget()
        pyqtGraphWidget = PyqtGraphWidget()

        graphSplitter = QSplitter()
        graphSplitter.setOrientation(Qt.Horizontal)
        graphSplitter.addWidget(pyqtGraphWidget)
        graphSplitter.addWidget(graphOptionsWidget)


        mainTabWidget.addTab(graphSplitter, 'Workspace 1')
        mainTabWidget.addTab(graphSplitter, 'Workspace 2')

        layout.addWidget(mainTabWidget)
        self.setLayout(layout)
        self.setAcceptDrops(True)


