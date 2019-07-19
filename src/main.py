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
        pixmap = QPixmap("REDCO_logo_1.png")
        smallerPixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = QSplashScreen(smallerPixmap, Qt.WindowStaysOnTopHint)
        # splash.setMask(smallerPixmap.mask())
        splash.show()
        splash.showMessage("Version check ...")
        time.sleep(1)
        self.processEvents()
        splash.showMessage("Loading DLLs ...")
        time.sleep(1)
        self.processEvents()
        splash.showMessage("Establishing SAP connection ...")
        time.sleep(1)
        self.processEvents()

    def newSplash(self):
        start = time.time()
        pixmap = QPixmap("images/ABB_logo.png")
        smallerPixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = LoadingDotsSplash(smallerPixmap)
        splash.setEnabled(False)
        splash.show()
        self.processEvents()
        while time.time() < start + 6:
            self.processEvents()

        splash.anim.close()


def main():
    # Makes the icon in the taskbar as well.
    appID = 'pyGrapher'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)

    app = App(sys.argv)
    app.setWindowIcon(QIcon("REDCO_icon_1_128.png"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
