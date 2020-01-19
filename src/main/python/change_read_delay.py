# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/change_read_delay.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog3(object):
    def setupUi(self, Dialog3):
        Dialog3.setObjectName("Dialog3")
        Dialog3.resize(400, 253)
        self.label = QtWidgets.QLabel(Dialog3)
        self.label.setGeometry(QtCore.QRect(10, 10, 361, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog3)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 381, 41))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog3)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 381, 121))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 200, 381, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog3)
        QtCore.QMetaObject.connectSlotsByName(Dialog3)

    def retranslateUi(self, Dialog3):
        _translate = QtCore.QCoreApplication.translate
        Dialog3.setWindowTitle(_translate("Dialog3", "Change Read Delay"))
        self.label.setText(_translate("Dialog3", "You can change the frequency the UI reads and updates data."))
        self.label_2.setText(_translate("Dialog3", "This affects both the local speed at which data is updated as well as how often data is requested from Google Sheets."))
        self.label_3.setText(_translate("Dialog3", "<html><head/><body><p>This is particularly useful in two scenarios:<br/>- You need to change the speed of the program to compensate for constantly increasing/decreasing lag time. Use this if the lag time becomes unacceptably high (or low?) over time.<br/>- You want to increase the speed of a replay (e.g. rerun a whole day\'s worth of data at 60x speed (not recommended)). The minimum is 125ms.</p></body></html>"))
        self.label_4.setText(_translate("Dialog3", "Read Delay (ms):"))
        self.pushButton.setText(_translate("Dialog3", "Apply"))

