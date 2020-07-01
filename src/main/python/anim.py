from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic, QtGui
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import pyqtSlot, QEasingCurve, QEventLoop, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QPalette

'''Fadable QLabel, as per https://stackoverflow.com/questions/48191399/pyqt-fading-a-qlabel.
Does not work if stylesheeted.

Consider looking into using QPalette or figuring out some other way to set the color of an individual AnimationLabel.
'''

class AnimationLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.animation = QtCore.QVariantAnimation()
        self.animation.valueChanged.connect(self.changeColor)

    @pyqtSlot(QtCore.QVariant)
    def changeColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)

    def startFadeIn(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 0))
        self.animation.setEndValue(QColor(0, 0, 0, 255))
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.start()

    def startFadeOut(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 255))
        self.animation.setEndValue(QColor(0, 0, 0, 0))
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()

    def startAnimation(self):
        self.startFadeIn()
        loop = QEventLoop()
        self.animation.finished.connect(loop.quit)
        loop.exec_()
        QTimer.singleShot(2000, self.startFadeOut)