from PyQt5.QtWidgets import QMainWindow
from gui.views.workspaceManagerView import WorkspaceManagerView
import os
from PyQt5 import uic

MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '\\mainWindowUi.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.mainGrapher = WorkspaceManagerView()
        self.setCentralWidget(self.mainGrapher)



