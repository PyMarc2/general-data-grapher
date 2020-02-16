from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QMovie, QIcon
from gui.mainWindow import MainWindow
import sys
import time
import ctypes
import threading


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = MainWindow()
        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setStyle("Fusion")
        self.setStyleSheet("")
        self.splash()
        self.main_view.show()
        self.main_view.setWindowTitle("PyGrapher")

    def splash(self):
        pixmap = QPixmap("media/pyg-icon-7.png")
        smaller_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = QSplashScreen(smaller_pixmap, Qt.WindowStaysOnTopHint)
        splash.show()
        time.sleep(3)


def main():
    # Makes the icon in the taskbar as well.
    appID = 'pyGrapher'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)

    app = App(sys.argv)
    app.setWindowIcon(QIcon("media/pyg-icon-7.png"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
