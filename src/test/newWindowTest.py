#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Main(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def mouseMoveEvent(self, event):
        # Enable mouse dragging
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def mousePressEvent(self, event):
        # Enable mouse dragging
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def keyPressEvent(self, event):
        # Escape key close the window
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        QtWidgets.QMainWindow.keyPressEvent(self, event)

    def paintEvent(self, event):
        # Draw a one pixel border
        borderColor = QtGui.QColor("black")
        bgColor = QtGui.QColor(self.palette().color(QtGui.QPalette.Background))
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(borderColor))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QtGui.QBrush(bgColor))
        painter.drawRect(1, 1, self.width()-2, self.height()-2)


if __name__== '__main__':
    app = QtWidgets.QApplication([])
    gui = Main(app)
    sys.exit(app.exec_())
