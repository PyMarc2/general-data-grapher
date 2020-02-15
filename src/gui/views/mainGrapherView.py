from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTabWidget, QFrame, QSplitter
from PyQt5.QtCore import pyqtSignal, Qt
from gui.widgets.dataManagerWidget import DataManagerWidget
from gui.widgets.graphOptionsWidget import GraphOptionsWidget
from gui.widgets.pyqtGraphWidget import PyqtGraphWidget
import os
from PyQt5 import uic

mainGrapherViewPath = os.path.dirname(os.path.realpath(__file__)) + '\\mainGrapherViewUi.ui'
Ui_mainGrapherView, QtBaseClass = uic.loadUiType(mainGrapherViewPath)


class MainGraphView(QWidget):
    def __init__(self):
        super(MainGraphView, self).__init__()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        mainTabWidget = QTabWidget()

        graphOptionsWidget = GraphOptionsWidget()
        pyqtGraphWidget = PyqtGraphWidget()
        dataViewerWidget = DataManagerWidget()
        dataManagerWidget = DataManagerWidget()

        graphSplitter = QSplitter()
        graphSplitter.setOrientation(Qt.Horizontal)
        graphSplitter.addWidget(pyqtGraphWidget)
        graphSplitter.addWidget(graphOptionsWidget)

        dataSplitter = QSplitter()
        dataSplitter.setOrientation(Qt.Horizontal)
        dataSplitter.addWidget(dataViewerWidget)
        dataSplitter.addWidget(dataManagerWidget)

        mainTabWidget.addTab(graphSplitter, 'Graph Tab')
        mainTabWidget.addTab(dataSplitter, 'Data Tab')

        layout.addWidget(mainTabWidget)
        self.setLayout(layout)


