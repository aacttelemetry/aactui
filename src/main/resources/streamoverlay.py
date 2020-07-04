# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamoverlay.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OverlayWindow(object):
    def setupUi(self, OverlayWindow):
        OverlayWindow.setObjectName("OverlayWindow")
        OverlayWindow.resize(1180, 951)
        self.centralwidget = QtWidgets.QWidget(OverlayWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(1158, 676))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setMinimumSize(QtCore.QSize(1152, 648))
        self.tab.setObjectName("tab")
        self.obstacle_remaining_label = AnimationLabel(self.tab)
        self.obstacle_remaining_label.setGeometry(QtCore.QRect(41, 271, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.obstacle_remaining_label.setFont(font)
        self.obstacle_remaining_label.setStyleSheet("color:white")
        self.obstacle_remaining_label.setObjectName("obstacle_remaining_label")
        self.test_background = QtWidgets.QLabel(self.tab)
        self.test_background.setGeometry(QtCore.QRect(0, 0, 1152, 648))
        self.test_background.setMinimumSize(QtCore.QSize(1152, 648))
        self.test_background.setText("")
        self.test_background.setPixmap(QtGui.QPixmap(":/images/background.png"))
        self.test_background.setScaledContents(True)
        self.test_background.setObjectName("test_background")
        self.obstacle_capital_label = AnimationLabel(self.tab)
        self.obstacle_capital_label.setGeometry(QtCore.QRect(21, 270, 21, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.obstacle_capital_label.setFont(font)
        self.obstacle_capital_label.setStyleSheet("color:white")
        self.obstacle_capital_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.obstacle_capital_label.setObjectName("obstacle_capital_label")
        self.obstacle_name_label = AnimationLabel(self.tab)
        self.obstacle_name_label.setGeometry(QtCore.QRect(28, 295, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.obstacle_name_label.setFont(font)
        self.obstacle_name_label.setStyleSheet("color:white")
        self.obstacle_name_label.setObjectName("obstacle_name_label")
        self.max_obstacle_points_label = AnimationLabel(self.tab)
        self.max_obstacle_points_label.setGeometry(QtCore.QRect(28, 315, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.max_obstacle_points_label.setFont(font)
        self.max_obstacle_points_label.setStyleSheet("color:white")
        self.max_obstacle_points_label.setObjectName("max_obstacle_points_label")
        self.static_points_label = AnimationLabel(self.tab)
        self.static_points_label.setGeometry(QtCore.QRect(176, 316, 290, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(8)
        self.static_points_label.setFont(font)
        self.static_points_label.setStyleSheet("color:white")
        self.static_points_label.setObjectName("static_points_label")
        self.static_time_label = AnimationLabel(self.tab)
        self.static_time_label.setGeometry(QtCore.QRect(82, 345, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_time_label.setFont(font)
        self.static_time_label.setStyleSheet("color:white")
        self.static_time_label.setObjectName("static_time_label")
        self.time_elapsed_label = AnimationLabel(self.tab)
        self.time_elapsed_label.setGeometry(QtCore.QRect(71, 368, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.time_elapsed_label.setFont(font)
        self.time_elapsed_label.setStyleSheet("color:white")
        self.time_elapsed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_elapsed_label.setObjectName("time_elapsed_label")
        self.efficiency_label = AnimationLabel(self.tab)
        self.efficiency_label.setGeometry(QtCore.QRect(71, 418, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.efficiency_label.setFont(font)
        self.efficiency_label.setStyleSheet("color:white")
        self.efficiency_label.setAlignment(QtCore.Qt.AlignCenter)
        self.efficiency_label.setObjectName("efficiency_label")
        self.static_efficiency_label = AnimationLabel(self.tab)
        self.static_efficiency_label.setGeometry(QtCore.QRect(95, 396, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_efficiency_label.setFont(font)
        self.static_efficiency_label.setStyleSheet("color:white")
        self.static_efficiency_label.setObjectName("static_efficiency_label")
        self.static_next_label = AnimationLabel(self.tab)
        self.static_next_label.setGeometry(QtCore.QRect(122, 461, 51, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_next_label.setFont(font)
        self.static_next_label.setStyleSheet("color:white")
        self.static_next_label.setObjectName("static_next_label")
        self.next_obstacle_label = AnimationLabel(self.tab)
        self.next_obstacle_label.setGeometry(QtCore.QRect(21, 484, 241, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.next_obstacle_label.setFont(font)
        self.next_obstacle_label.setStyleSheet("color:white")
        self.next_obstacle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_obstacle_label.setObjectName("next_obstacle_label")
        self.variable_capital_label = AnimationLabel(self.tab)
        self.variable_capital_label.setGeometry(QtCore.QRect(622, 520, 21, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.variable_capital_label.setFont(font)
        self.variable_capital_label.setStyleSheet("color:white")
        self.variable_capital_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.variable_capital_label.setObjectName("variable_capital_label")
        self.variable_remaining_label = AnimationLabel(self.tab)
        self.variable_remaining_label.setGeometry(QtCore.QRect(643, 521, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.variable_remaining_label.setFont(font)
        self.variable_remaining_label.setStyleSheet("color:white")
        self.variable_remaining_label.setObjectName("variable_remaining_label")
        self.current_speed_label = AnimationLabel(self.tab)
        self.current_speed_label.setGeometry(QtCore.QRect(920, 470, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_speed_label.setFont(font)
        self.current_speed_label.setStyleSheet("color:white")
        self.current_speed_label.setObjectName("current_speed_label")
        self.current_heartrate_label = AnimationLabel(self.tab)
        self.current_heartrate_label.setGeometry(QtCore.QRect(1058, 469, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_heartrate_label.setFont(font)
        self.current_heartrate_label.setStyleSheet("color:white")
        self.current_heartrate_label.setObjectName("current_heartrate_label")
        self.debug_label = AnimationLabel(self.tab)
        self.debug_label.setGeometry(QtCore.QRect(820, 10, 321, 161))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.debug_label.setFont(font)
        self.debug_label.setStyleSheet("color:white")
        self.debug_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.debug_label.setObjectName("debug_label")
        self.gps_label = AnimationLabel(self.tab)
        self.gps_label.setGeometry(QtCore.QRect(24, 157, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.gps_label.setFont(font)
        self.gps_label.setStyleSheet("color:white")
        self.gps_label.setObjectName("gps_label")
        self.static_disp_label = AnimationLabel(self.tab)
        self.static_disp_label.setGeometry(QtCore.QRect(23, 202, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.static_disp_label.setFont(font)
        self.static_disp_label.setStyleSheet("color:white")
        self.static_disp_label.setObjectName("static_disp_label")
        self.relative_position_label = AnimationLabel(self.tab)
        self.relative_position_label.setGeometry(QtCore.QRect(69, 190, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.relative_position_label.setFont(font)
        self.relative_position_label.setStyleSheet("color:white")
        self.relative_position_label.setObjectName("relative_position_label")
        self.relative_error_label = AnimationLabel(self.tab)
        self.relative_error_label.setGeometry(QtCore.QRect(68, 212, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.relative_error_label.setFont(font)
        self.relative_error_label.setStyleSheet("color:white")
        self.relative_error_label.setObjectName("relative_error_label")
        self.max_points_label = AnimationLabel(self.tab)
        self.max_points_label.setGeometry(QtCore.QRect(212, 290, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.max_points_label.setFont(font)
        self.max_points_label.setStyleSheet("color:white")
        self.max_points_label.setObjectName("max_points_label")
        self.current_points_label = AnimationLabel(self.tab)
        self.current_points_label.setGeometry(QtCore.QRect(113, 271, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_points_label.setFont(font)
        self.current_points_label.setStyleSheet("color:white")
        self.current_points_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.current_points_label.setObjectName("current_points_label")
        self.test_background.raise_()
        self.obstacle_remaining_label.raise_()
        self.obstacle_capital_label.raise_()
        self.obstacle_name_label.raise_()
        self.max_obstacle_points_label.raise_()
        self.static_points_label.raise_()
        self.static_time_label.raise_()
        self.time_elapsed_label.raise_()
        self.efficiency_label.raise_()
        self.static_efficiency_label.raise_()
        self.static_next_label.raise_()
        self.next_obstacle_label.raise_()
        self.variable_capital_label.raise_()
        self.variable_remaining_label.raise_()
        self.current_speed_label.raise_()
        self.current_heartrate_label.raise_()
        self.debug_label.raise_()
        self.gps_label.raise_()
        self.static_disp_label.raise_()
        self.relative_position_label.raise_()
        self.relative_error_label.raise_()
        self.max_points_label.raise_()
        self.current_points_label.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.relative_error_label_2 = AnimationLabel(self.tab_2)
        self.relative_error_label_2.setGeometry(QtCore.QRect(55, 211, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.relative_error_label_2.setFont(font)
        self.relative_error_label_2.setObjectName("relative_error_label_2")
        self.static_disp_label_2 = AnimationLabel(self.tab_2)
        self.static_disp_label_2.setGeometry(QtCore.QRect(10, 201, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.static_disp_label_2.setFont(font)
        self.static_disp_label_2.setObjectName("static_disp_label_2")
        self.debug_label_2 = AnimationLabel(self.tab_2)
        self.debug_label_2.setGeometry(QtCore.QRect(807, 9, 321, 161))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.debug_label_2.setFont(font)
        self.debug_label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.debug_label_2.setObjectName("debug_label_2")
        self.max_obstacle_points_label_2 = AnimationLabel(self.tab_2)
        self.max_obstacle_points_label_2.setGeometry(QtCore.QRect(15, 314, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.max_obstacle_points_label_2.setFont(font)
        self.max_obstacle_points_label_2.setObjectName("max_obstacle_points_label_2")
        self.variable_capital_label_2 = AnimationLabel(self.tab_2)
        self.variable_capital_label_2.setGeometry(QtCore.QRect(609, 519, 21, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.variable_capital_label_2.setFont(font)
        self.variable_capital_label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.variable_capital_label_2.setObjectName("variable_capital_label_2")
        self.max_points_label_2 = AnimationLabel(self.tab_2)
        self.max_points_label_2.setGeometry(QtCore.QRect(199, 289, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.max_points_label_2.setFont(font)
        self.max_points_label_2.setObjectName("max_points_label_2")
        self.current_heartrate_label_2 = AnimationLabel(self.tab_2)
        self.current_heartrate_label_2.setGeometry(QtCore.QRect(1045, 468, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_heartrate_label_2.setFont(font)
        self.current_heartrate_label_2.setObjectName("current_heartrate_label_2")
        self.obstacle_capital_label_2 = AnimationLabel(self.tab_2)
        self.obstacle_capital_label_2.setGeometry(QtCore.QRect(8, 269, 21, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.obstacle_capital_label_2.setFont(font)
        self.obstacle_capital_label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.obstacle_capital_label_2.setObjectName("obstacle_capital_label_2")
        self.obstacle_name_label_2 = AnimationLabel(self.tab_2)
        self.obstacle_name_label_2.setGeometry(QtCore.QRect(15, 294, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.obstacle_name_label_2.setFont(font)
        self.obstacle_name_label_2.setObjectName("obstacle_name_label_2")
        self.efficiency_label_2 = AnimationLabel(self.tab_2)
        self.efficiency_label_2.setGeometry(QtCore.QRect(58, 417, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.efficiency_label_2.setFont(font)
        self.efficiency_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.efficiency_label_2.setObjectName("efficiency_label_2")
        self.static_points_label_2 = AnimationLabel(self.tab_2)
        self.static_points_label_2.setGeometry(QtCore.QRect(163, 315, 290, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(8)
        self.static_points_label_2.setFont(font)
        self.static_points_label_2.setObjectName("static_points_label_2")
        self.static_time_label_2 = AnimationLabel(self.tab_2)
        self.static_time_label_2.setGeometry(QtCore.QRect(69, 344, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_time_label_2.setFont(font)
        self.static_time_label_2.setObjectName("static_time_label_2")
        self.next_obstacle_label_2 = AnimationLabel(self.tab_2)
        self.next_obstacle_label_2.setGeometry(QtCore.QRect(8, 483, 241, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(9)
        self.next_obstacle_label_2.setFont(font)
        self.next_obstacle_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.next_obstacle_label_2.setObjectName("next_obstacle_label_2")
        self.static_efficiency_label_2 = AnimationLabel(self.tab_2)
        self.static_efficiency_label_2.setGeometry(QtCore.QRect(82, 395, 131, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_efficiency_label_2.setFont(font)
        self.static_efficiency_label_2.setObjectName("static_efficiency_label_2")
        self.obstacle_remaining_label_2 = AnimationLabel(self.tab_2)
        self.obstacle_remaining_label_2.setGeometry(QtCore.QRect(28, 270, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.obstacle_remaining_label_2.setFont(font)
        self.obstacle_remaining_label_2.setObjectName("obstacle_remaining_label_2")
        self.gps_label_2 = AnimationLabel(self.tab_2)
        self.gps_label_2.setGeometry(QtCore.QRect(11, 156, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.gps_label_2.setFont(font)
        self.gps_label_2.setObjectName("gps_label_2")
        self.current_points_label_2 = AnimationLabel(self.tab_2)
        self.current_points_label_2.setGeometry(QtCore.QRect(100, 270, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_points_label_2.setFont(font)
        self.current_points_label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.current_points_label_2.setObjectName("current_points_label_2")
        self.time_elapsed_label_2 = AnimationLabel(self.tab_2)
        self.time_elapsed_label_2.setGeometry(QtCore.QRect(58, 367, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(14)
        self.time_elapsed_label_2.setFont(font)
        self.time_elapsed_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.time_elapsed_label_2.setObjectName("time_elapsed_label_2")
        self.current_speed_label_2 = AnimationLabel(self.tab_2)
        self.current_speed_label_2.setGeometry(QtCore.QRect(907, 469, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.current_speed_label_2.setFont(font)
        self.current_speed_label_2.setObjectName("current_speed_label_2")
        self.static_next_label_2 = AnimationLabel(self.tab_2)
        self.static_next_label_2.setGeometry(QtCore.QRect(109, 460, 51, 50))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(10)
        self.static_next_label_2.setFont(font)
        self.static_next_label_2.setObjectName("static_next_label_2")
        self.relative_position_label_2 = AnimationLabel(self.tab_2)
        self.relative_position_label_2.setGeometry(QtCore.QRect(56, 189, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.relative_position_label_2.setFont(font)
        self.relative_position_label_2.setObjectName("relative_position_label_2")
        self.variable_remaining_label_2 = AnimationLabel(self.tab_2)
        self.variable_remaining_label_2.setGeometry(QtCore.QRect(630, 520, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        self.variable_remaining_label_2.setFont(font)
        self.variable_remaining_label_2.setObjectName("variable_remaining_label_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cumulative_position_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.cumulative_position_checkbox.setObjectName("cumulative_position_checkbox")
        self.verticalLayout_3.addWidget(self.cumulative_position_checkbox)
        self.gps_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.gps_checkbox.setObjectName("gps_checkbox")
        self.verticalLayout_3.addWidget(self.gps_checkbox)
        self.displacement_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.displacement_checkbox.setObjectName("displacement_checkbox")
        self.verticalLayout_3.addWidget(self.displacement_checkbox)
        self.environmental_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.environmental_checkbox.setObjectName("environmental_checkbox")
        self.verticalLayout_3.addWidget(self.environmental_checkbox)
        self.athelete_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.athelete_checkbox.setObjectName("athelete_checkbox")
        self.verticalLayout_3.addWidget(self.athelete_checkbox)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.debug_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.debug_checkbox.setToolTip("")
        self.debug_checkbox.setObjectName("debug_checkbox")
        self.verticalLayout_2.addWidget(self.debug_checkbox)
        self.data_read_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.data_read_checkbox.setToolTip("")
        self.data_read_checkbox.setObjectName("data_read_checkbox")
        self.verticalLayout_2.addWidget(self.data_read_checkbox)
        self.competition_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.competition_checkbox.setObjectName("competition_checkbox")
        self.verticalLayout_2.addWidget(self.competition_checkbox)
        self.orientation_display_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.orientation_display_checkbox.setObjectName("orientation_display_checkbox")
        self.verticalLayout_2.addWidget(self.orientation_display_checkbox)
        self.orientation_text_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.orientation_text_checkbox.setObjectName("orientation_text_checkbox")
        self.verticalLayout_2.addWidget(self.orientation_text_checkbox)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.gps_point_radio = QtWidgets.QRadioButton(self.groupBox)
        self.gps_point_radio.setObjectName("gps_point_radio")
        self.verticalLayout_4.addWidget(self.gps_point_radio)
        self.relative_point_radio = QtWidgets.QRadioButton(self.groupBox)
        self.relative_point_radio.setObjectName("relative_point_radio")
        self.verticalLayout_4.addWidget(self.relative_point_radio)
        self.gps_lines_radio = QtWidgets.QRadioButton(self.groupBox)
        self.gps_lines_radio.setObjectName("gps_lines_radio")
        self.verticalLayout_4.addWidget(self.gps_lines_radio)
        self.relative_lines_radio = QtWidgets.QRadioButton(self.groupBox)
        self.relative_lines_radio.setObjectName("relative_lines_radio")
        self.verticalLayout_4.addWidget(self.relative_lines_radio)
        self.cycle_all_radio = QtWidgets.QRadioButton(self.groupBox)
        self.cycle_all_radio.setObjectName("cycle_all_radio")
        self.verticalLayout_4.addWidget(self.cycle_all_radio)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 1, 1, 1)
        self.keyable_hex_value = QtWidgets.QLineEdit(self.groupBox)
        self.keyable_hex_value.setObjectName("keyable_hex_value")
        self.gridLayout_2.addWidget(self.keyable_hex_value, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 2)
        self.browser_radio = QtWidgets.QRadioButton(self.groupBox)
        self.browser_radio.setObjectName("browser_radio")
        self.gridLayout_2.addWidget(self.browser_radio, 4, 0, 1, 1)
        self.fade_duration_value = QtWidgets.QLineEdit(self.groupBox)
        self.fade_duration_value.setObjectName("fade_duration_value")
        self.gridLayout_2.addWidget(self.fade_duration_value, 1, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 2)
        self.keyable_radio = QtWidgets.QRadioButton(self.groupBox)
        self.keyable_radio.setObjectName("keyable_radio")
        self.gridLayout_2.addWidget(self.keyable_radio, 5, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.start_updating_button = QtWidgets.QPushButton(self.groupBox)
        self.start_updating_button.setObjectName("start_updating_button")
        self.verticalLayout_5.addWidget(self.start_updating_button)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout.addWidget(self.groupBox)
        OverlayWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OverlayWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1180, 26))
        self.menubar.setObjectName("menubar")
        OverlayWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OverlayWindow)
        self.statusbar.setObjectName("statusbar")
        OverlayWindow.setStatusBar(self.statusbar)

        self.retranslateUi(OverlayWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(OverlayWindow)

    def retranslateUi(self, OverlayWindow):
        _translate = QtCore.QCoreApplication.translate
        OverlayWindow.setWindowTitle(_translate("OverlayWindow", "MainWindow"))
        self.obstacle_remaining_label.setText(_translate("OverlayWindow", "BSTACLE 6"))
        self.obstacle_capital_label.setText(_translate("OverlayWindow", "O"))
        self.obstacle_name_label.setText(_translate("OverlayWindow", "OBSTACLE NAME"))
        self.max_obstacle_points_label.setText(_translate("OverlayWindow", "12 POINTS MAX"))
        self.static_points_label.setText(_translate("OverlayWindow", "POINTS (EST.)"))
        self.static_time_label.setText(_translate("OverlayWindow", "TIME ELAPSED:"))
        self.time_elapsed_label.setText(_translate("OverlayWindow", "0:00 (0:00)"))
        self.efficiency_label.setText(_translate("OverlayWindow", "0.4 pps"))
        self.static_efficiency_label.setText(_translate("OverlayWindow", "EFFICIENCY:"))
        self.static_next_label.setText(_translate("OverlayWindow", "NEXT:"))
        self.next_obstacle_label.setText(_translate("OverlayWindow", "OBSTACLE # - OBSTACLE NAME"))
        self.variable_capital_label.setText(_translate("OverlayWindow", "E"))
        self.variable_remaining_label.setText(_translate("OverlayWindow", "NVIRONMENTAL DATA"))
        self.current_speed_label.setText(_translate("OverlayWindow", "14 m/s"))
        self.current_heartrate_label.setText(_translate("OverlayWindow", "134 bpm"))
        self.debug_label.setText(_translate("OverlayWindow", "debug"))
        self.gps_label.setText(_translate("OverlayWindow", "GPS: 15.123456, -15.123456"))
        self.static_disp_label.setText(_translate("OverlayWindow", "DISP:"))
        self.relative_position_label.setText(_translate("OverlayWindow", "16.123456, -16.123456"))
        self.relative_error_label.setText(_translate("OverlayWindow", "+124.5 ft, -124.5 ft"))
        self.max_points_label.setText(_translate("OverlayWindow", "120"))
        self.current_points_label.setText(_translate("OverlayWindow", "5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("OverlayWindow", "Overlay 1"))
        self.relative_error_label_2.setText(_translate("OverlayWindow", "+124.5 ft, -124.5 ft"))
        self.static_disp_label_2.setText(_translate("OverlayWindow", "DISP:"))
        self.debug_label_2.setText(_translate("OverlayWindow", "debug"))
        self.max_obstacle_points_label_2.setText(_translate("OverlayWindow", "12 POINTS MAX"))
        self.variable_capital_label_2.setText(_translate("OverlayWindow", "E"))
        self.max_points_label_2.setText(_translate("OverlayWindow", "120"))
        self.current_heartrate_label_2.setText(_translate("OverlayWindow", "134 bpm"))
        self.obstacle_capital_label_2.setText(_translate("OverlayWindow", "O"))
        self.obstacle_name_label_2.setText(_translate("OverlayWindow", "OBSTACLE NAME"))
        self.efficiency_label_2.setText(_translate("OverlayWindow", "0.4 pps"))
        self.static_points_label_2.setText(_translate("OverlayWindow", "POINTS (EST.)"))
        self.static_time_label_2.setText(_translate("OverlayWindow", "TIME ELAPSED:"))
        self.next_obstacle_label_2.setText(_translate("OverlayWindow", "OBSTACLE # - OBSTACLE NAME"))
        self.static_efficiency_label_2.setText(_translate("OverlayWindow", "EFFICIENCY:"))
        self.obstacle_remaining_label_2.setText(_translate("OverlayWindow", "BSTACLE 6"))
        self.gps_label_2.setText(_translate("OverlayWindow", "GPS: 15.123456, -15.123456"))
        self.current_points_label_2.setText(_translate("OverlayWindow", "5"))
        self.time_elapsed_label_2.setText(_translate("OverlayWindow", "0:00 (0:00)"))
        self.current_speed_label_2.setText(_translate("OverlayWindow", "14 m/s"))
        self.static_next_label_2.setText(_translate("OverlayWindow", "NEXT:"))
        self.relative_position_label_2.setText(_translate("OverlayWindow", "16.123456, -16.123456"))
        self.variable_remaining_label_2.setText(_translate("OverlayWindow", "NVIRONMENTAL DATA"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("OverlayWindow", "Overlay 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("OverlayWindow", "Large Map"))
        self.groupBox.setTitle(_translate("OverlayWindow", "GroupBox"))
        self.label.setText(_translate("OverlayWindow", "Show:"))
        self.cumulative_position_checkbox.setText(_translate("OverlayWindow", "Cumulative positioning data"))
        self.gps_checkbox.setText(_translate("OverlayWindow", "Additional GPS data"))
        self.displacement_checkbox.setText(_translate("OverlayWindow", "Displacement"))
        self.environmental_checkbox.setText(_translate("OverlayWindow", "Environmental data"))
        self.athelete_checkbox.setText(_translate("OverlayWindow", "Athlete data"))
        self.debug_checkbox.setText(_translate("OverlayWindow", "Debug"))
        self.data_read_checkbox.setText(_translate("OverlayWindow", "Data read/send status"))
        self.competition_checkbox.setToolTip(_translate("OverlayWindow", "Show minimalist map overlaying GPS data."))
        self.competition_checkbox.setText(_translate("OverlayWindow", "Competition data"))
        self.orientation_display_checkbox.setText(_translate("OverlayWindow", "Orientation, display"))
        self.orientation_text_checkbox.setText(_translate("OverlayWindow", "Orientation, text"))
        self.label_5.setText(_translate("OverlayWindow", "Displacement:"))
        self.gps_point_radio.setText(_translate("OverlayWindow", "GPS, single point"))
        self.relative_point_radio.setText(_translate("OverlayWindow", "Relative, single point"))
        self.gps_lines_radio.setText(_translate("OverlayWindow", "GPS, lines"))
        self.relative_lines_radio.setText(_translate("OverlayWindow", "Relative, lines"))
        self.cycle_all_radio.setText(_translate("OverlayWindow", "Cycle all"))
        self.label_4.setText(_translate("OverlayWindow", "Color for keyable (hex):"))
        self.label_3.setText(_translate("OverlayWindow", "Use:"))
        self.browser_radio.setText(_translate("OverlayWindow", "Internal browser"))
        self.label_2.setText(_translate("OverlayWindow", "Fade duration (ms):"))
        self.keyable_radio.setText(_translate("OverlayWindow", "Keyable background"))
        self.start_updating_button.setText(_translate("OverlayWindow", "Start updating elements"))
        self.pushButton.setToolTip(_translate("OverlayWindow", "Click for help on setting up the stream, including keys and information."))
        self.pushButton.setText(_translate("OverlayWindow", "I need help"))
from anim import AnimationLabel
import res_rc
