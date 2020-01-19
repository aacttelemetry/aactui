# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/change_max_graph_values.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog4(object):
    def setupUi(self, Dialog4):
        Dialog4.setObjectName("Dialog4")
        Dialog4.resize(400, 173)
        self.label = QtWidgets.QLabel(Dialog4)
        self.label.setGeometry(QtCore.QRect(10, 10, 361, 51))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog4)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 120, 381, 41))
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
        self.label_2 = QtWidgets.QLabel(Dialog4)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 381, 51))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog4)
        QtCore.QMetaObject.connectSlotsByName(Dialog4)

    def retranslateUi(self, Dialog4):
        _translate = QtCore.QCoreApplication.translate
        Dialog4.setWindowTitle(_translate("Dialog4", "Change Max Graph Values"))
        self.label.setText(_translate("Dialog4", "You can change the maximum values on the humidity and temperature graphs, enlarging the window of time they represent."))
        self.label_4.setText(_translate("Dialog4", "Max Values:"))
        self.pushButton.setText(_translate("Dialog4", "Apply"))
        self.label_2.setText(_translate("Dialog4", "While there is no upper limit, you should be aware of your computer\'s limitations - too many values will eventually cause the program to begin lagging."))

