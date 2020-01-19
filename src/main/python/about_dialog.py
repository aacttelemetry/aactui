# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog2(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(575, 164)
        self.label = QtWidgets.QLabel(Dialog2)
        self.label.setGeometry(QtCore.QRect(10, 10, 501, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog2)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 541, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog2)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 541, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog2)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 541, 41))
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Dialog2)
        self.label_6.setGeometry(QtCore.QRect(10, 140, 541, 16))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog2)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        _translate = QtCore.QCoreApplication.translate
        Dialog2.setWindowTitle(_translate("Dialog2", "About"))
        self.label.setText(_translate("Dialog2", "Telemetry UI developed for the NASA Human Exploration Rover Challenge, 2019."))
        self.label_2.setText(_translate("Dialog2", "Made with PyQt5, matplotlib, Pillow, and google-api-python-client; built and packaged with fbs."))
        self.label_3.setText(_translate("Dialog2", "Developed at (and for) the Academy of Arts, Careers, and Technology in Reno, Nevada."))
        self.label_4.setText(_translate("Dialog2", "<html><head/><body><p>You can view the source code of the project, as well as any future improvements, <a href=\"https://github.com/lgactna/aact-telemetry\"><span style=\" text-decoration: underline; color:#0000ff;\">here.</span></a> (you may have to right-click and click &quot;Copy Link Location&quot;)</p></body></html>"))
        self.label_6.setText(_translate("Dialog2", "Special thanks to everyone who made this possible."))

