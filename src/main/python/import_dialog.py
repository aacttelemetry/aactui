# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/import_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 187)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 331, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 381, 61))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 381, 31))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 140, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(79, 140, 114, 29))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 140, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Import .db file?"))
        self.label.setText(_translate("Dialog", "Selected file:"))
        self.label_2.setText(_translate("Dialog", "-"))
        self.label_3.setText(_translate("Dialog", "If you import a database file, the UI will be locked to this file until it is closed. If you want to read from Google Sheets, either restart the UI or run another instance."))
        self.label_4.setText(_translate("Dialog", "Also, if this file is invalid (or a non-telemetry .db), you\'ll probably crash the UI."))
        self.pushButton_2.setText(_translate("Dialog", "Yes"))
        self.label_5.setText(_translate("Dialog", "Continue importing?"))
        self.pushButton.setText(_translate("Dialog", "No"))

