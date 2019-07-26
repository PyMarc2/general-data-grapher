from PyQt5.QtWidgets import QLineEdit, QWidget, QDialog, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QDesktopWidget
from PyQt5.Qt import QVariantAnimation, QSplashScreen, QSize, QEvent, QResizeEvent, QMouseEvent, QRectF, QSizeF
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QEasingCurve, QTimer, QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtGui import QPainter, QLinearGradient
from PyQt5 import QtGui
from PyQt5 import QtCore
from functools import partial

#   |=========================================|
#   |                 QWIDGETS                |
#   |=========================================|


class CustomLineEdit(QLineEdit):

    @property
    def backgroundColor(self):
        return self._backgroundColor
    @backgroundColor.setter
    def backgroundColor(self, color):
        self.setStyleSheet("background-color: {}".format(color.name()))

    def __init__(self, qtObject):
        super(CustomLineEdit, self).__init__(qtObject)

    def redFlash(self):
        self.anim_redFlash = QVariantAnimation(self, startValue=QColor(255, 127, 127),
                                                     endValue=QColor(255, 255, 255),
                                                     duration=1000)
        self.anim_redFlash.valueChanged.connect(self.changeBackground)
        self.anim_redFlash.start()

    def changeBackground(self, color):
        self.backgroundColor = color


class CustomQBar(QWidget):
    pass

#   |=========================================|
#   |                 ANIMATION               |
#   |=========================================|


class QVariantAnimationBetter(QVariantAnimation):

    valueChangedBetter = pyqtSignal(list)

    def __init__(self, Object, startValue=0, endValue=0, duration=0):
        super(QVariantAnimationBetter, self).__init__(Object, startValue=startValue, endValue=endValue, duration=duration)
        self.object = Object
        self.valueChanged.connect(self.sendAnimationObjectSignal)

    def sendAnimationObjectSignal(self, value):
        self.valueChangedBetter.emit([self.object, value])


class LoadingDotsWidget(QWidget):

    s_externalRepaint = pyqtSignal()

    def __init__(self, parent, amount=3, radius=7, speed=150, sep=0, xpos=0, ypos=0, xsize=0, offsetx=0, offsety=0, easingcurve=QEasingCurve.OutInCubic, isLooping=True, loopingOn=3):
        super(LoadingDotsWidget, self).__init__(parent)
        self.offsetx = offsetx
        self.offsety = offsety
        self.isLooping = isLooping
        self.loopingOn = loopingOn
        self.yPosition = ypos

        self.dotsRadius = radius
        self.dotsColor = QColor(255, 0, 15)
        self.dotsAmount = amount
        self.dotsSpeed = speed
        self.dotsSeparation = sep

        # ANIMATION PARAMETERS
        self.userEasingCurve = easingcurve
        self.animationSize = xsize
        self.separationTime = int((self.dotsSeparation / self.dotsSpeed) * 1000)
        print(self.separationTime)
        self.dotsPosition = []
        self.dotsAnimations = []

        self.createPosition()
        self.createAnimation()

    def startMoving(self):
        # print(self.dotsAnimations)
        timer = QTimer()
        timer.setTimerType(0)
        for i, animation in enumerate(self.dotsAnimations):
            timer.singleShot(i*self.separationTime, animation.start)

    def createPosition(self):
        for i in range(self.dotsAmount):
            self.dotsPosition.append(QPoint(-10, self.yPosition))

    def createAnimation(self):
        duration = (self.animationSize / self.dotsSpeed)*1000

        for i, _ in enumerate(self.dotsPosition):
            anim = QVariantAnimation(self, startValue=0, endValue=self.animationSize,
                                            duration=duration, easingCurve=self.userEasingCurve)
            wrapper = partial(self.updatePosition, i)
            anim.valueChanged.connect(wrapper)

            if self.isLooping and self.loopingOn == i+1:
                anim.finished.connect(self.startMoving)

            self.dotsAnimations.append(anim)

    @QtCore.pyqtSlot(int, QtCore.QVariant)
    def updatePosition(self, i, position):
        try:
            self.dotsPosition[i] = QtCore.QPoint(position+self.offsetx, self.yPosition)
        except AttributeError as err:
            pass
        self.s_externalRepaint.emit()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        for i, position in enumerate(self.dotsPosition):
            painter.setBrush(
                QtGui.QBrush(self.dotsColor, QtCore.Qt.SolidPattern)
            )
            painter.drawEllipse(position, self.dotsRadius, self.dotsRadius)
            print(position, i)


class LoadingDotsSplash(QSplashScreen):
    def __init__(self, image):
        self.isRunning = True
        self.image = image
        self.frame = QPixmap(image.rect().size() + QSize(0, 20))
        self.frame.fill(Qt.transparent)
        QSplashScreen.__init__(self, self.frame, QtCore.Qt.WindowStaysOnTopHint)

        # COMPARISON BETWEEN EASING CURVES
        easingCurve = QEasingCurve()
        easingCurve.setCustomType(self.funkyEasingFunc)
        self.anim = LoadingDotsWidget(None, ypos=110, xsize=self.image.rect().size().width()+10, sep=40, offsetx=0, speed=100, easingcurve=easingCurve, amount=3, loopingOn=3)
        self.anim.s_externalRepaint.connect(self.update)
        self.frameSize = self.rect().size() + QSize(0, 20)

    def showEvent(self, event):
        self.anim.startMoving()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPixmap(self.image.rect(), self.image)
        painter.setBrush(QtGui.QBrush(self.anim.dotsColor, QtCore.Qt.SolidPattern))

        for i, position in enumerate(self.anim.dotsPosition):
            painter.drawEllipse(position, self.anim.dotsRadius, self.anim.dotsRadius)
            print(position, i)

    @staticmethod
    def customEasingFunc(x):
        return 3.3 * (x - 0.51) ** 3 + 0.2 * (x - 7.9) + 2

    @staticmethod
    def customCenteredEasingFunc(x):
        return 2.3 * (x - 0.51) ** 3 + 0.4 * (x - 7.9) + 3.45

    @staticmethod
    def customTestEasingFunc(x):
        return 2.42 * (x - 0.515) ** 3 + 0.4 * (x - 7.7) + 3.4

    @staticmethod
    def lastEasingFunc(x):
        return 3.3*(x-0.5)**3 + 0.20*(x-7.9)+1.98

    @staticmethod
    def funkyEasingFunc(x):
        return 7000 * (x - 0.505) ** 15 + 1 * (x - 0.5) ** 9 + 5 * (x - 0.45) ** 7 + 0 * (x - 0.33) ** 5 + 0 * (
                x - 0.33) ** 3 + 0.5 * (x - 7.9) + 4.2

    @staticmethod
    def superfunkyEasingFunc(x):
        return 2 * (x - 0.505) ** 13 + 2 * (x - 0.505) ** 11 + 2 * (x - 0.5) ** 9 + 1 * (x - 0.45) ** 7 + 1 * (
                x - 0.33) ** 5 + 2 * (x - 0.5) ** 3 + 0.3 * (x - 7.9) + 2.65

#   |=========================================|
#   |                 QWINDOWS                |
#   |=========================================|


class QRoundedWindow(QWidget):

    def __init__(self):
        super(QRoundedWindow, self).__init__()
        self.cornerSize = 10.0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.begin(self)
        painter.setBrush(self.palette().window())
        painter.drawRoundedRect(QRectF(self.rect()), self.cornerSize, self.cornerSize)
        painter.end()


class QCustomDialog(QDialog):
    s_windowClose = pyqtSignal()

    @property
    def isBackgroundEnabled(self):
        return self._isBackgroundEnabled

    @isBackgroundEnabled.setter
    def isBackgroundEnabled(self, value: bool):
        self._isBackgroundEnabled = value

    @property
    def isFadeInOpacityEnabled(self):
        return self._isFadeInOpacityEnabled

    @isFadeInOpacityEnabled.setter
    def isFadeInOpacityEnabled(self, value: bool):
        self._isFadeInOpacityEnabled = value

    @property
    def isFadeInPositionEnabled(self):
        return self._isFadeInPositionEnabled

    @isFadeInPositionEnabled.setter
    def isFadeInPositionEnabled(self, value: bool):
        self._isFadeInPositionEnabled = value

    @property
    def fadeDuration(self):
        return self._fadeDuration

    @fadeDuration.setter
    def fadeDuration(self, value: int):
        self._fadeDuration = value

    @property
    def isAlwaysOnTop(self):
        return self._isAlwaysOnTop

    @isAlwaysOnTop.setter
    def isAlwaysOnTop(self, value: bool):
        self._isAlwaysOnTop = value
        self.setWindowFlag(Qt.WindowStaysOnTopHint, value)

    @property
    def isFrameless(self):
        return self._isFrameless

    @isFrameless.setter
    def isFrameless(self, value: bool):
        self._isFrameless = value
        self.setWindowFlag(Qt.FramelessWindowHint, value)

    def __init__(self):
        super(QCustomDialog, self).__init__()

        self._isBackgroundEnabled = True
        self._isFadeInOpacityEnabled = True
        self._isFadeInPositionEnabled = True
        self._fadeDuration = 300
        self._isAlwaysOnTop = None
        self._isFrameless = None
        self.isFrameless = True
        self.isAlwaysOnTop = True

        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupBackground()
        self.setupFadeInOpacity()

    def setupBackground(self):
        self.backGround = QDialog()
        self.backGround.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.backGround.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.backGround.setWindowOpacity(0.5)
        self.backGround.setEnabled(False)

    def setupFadeInOpacity(self):
        self.fadeInOpacityAnimation = QtCore.QPropertyAnimation()
        self.fadeInOpacityAnimation.setTargetObject(self)
        self.fadeInOpacityAnimation.setPropertyName(b"windowOpacity")
        self.fadeInOpacityAnimation.setDuration(self.fadeDuration)
        self.fadeInOpacityAnimation.setStartValue(0.0)
        self.fadeInOpacityAnimation.setEndValue(1.0)

    def setupFadeInPosition(self):
        # Must be executed inside the child object
        ag = QDesktopWidget().availableGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        centerPosition = QPoint(int(cp.x()-(self.frameGeometry().width()/2)), int(cp.y()-(self.frameGeometry().height()/2)))
        startPosition = QPoint(centerPosition.x(), centerPosition.y()+(int(ag.height()*0.07)))
        self.fadeInPositionAnimation = QtCore.QPropertyAnimation()
        self.fadeInPositionAnimation.setTargetObject(self)
        self.fadeInPositionAnimation.setPropertyName(b"pos")
        self.fadeInPositionAnimation.setDuration(self.fadeDuration)
        self.fadeInPositionAnimation.setStartValue(startPosition)
        self.fadeInPositionAnimation.setEndValue(centerPosition)

    def fade_in_opacity(self):
        if self.isFadeInOpacityEnabled:
            self.fadeInOpacityAnimation.start()

    def fade_in_position(self):
        if self.isFadeInPositionEnabled:
            self.fadeInPositionAnimation.start()

    def showEvent(self, event):
        if self.isBackgroundEnabled:
            self.backGround.showFullScreen()
        self.fade_in_opacity()
        self.fade_in_position()

    def closeEvent(self, event):
        self.backGround.close()
        self.s_windowClose.emit()




