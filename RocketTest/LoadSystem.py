# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadSystem.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1888, 1014)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(1700, 931, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.StartButton.setFont(font)
        self.StartButton.setObjectName("StartButton")
        self.LoadButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadButton.setGeometry(QtCore.QRect(1700, 320, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.LoadButton.setFont(font)
        self.LoadButton.setObjectName("LoadButton")
        self.Filename_field = QtWidgets.QLineEdit(self.centralwidget)
        self.Filename_field.setGeometry(QtCore.QRect(1700, 110, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Filename_field.setFont(font)
        self.Filename_field.setObjectName("Filename_field")
        self.EngineBar = QtWidgets.QScrollBar(self.centralwidget)
        self.EngineBar.setGeometry(QtCore.QRect(1700, 440, 31, 361))
        self.EngineBar.setMaximum(100)
        self.EngineBar.setPageStep(8)
        self.EngineBar.setOrientation(QtCore.Qt.Vertical)
        self.EngineBar.setObjectName("EngineBar")
        self.AngleBar = QtWidgets.QDial(self.centralwidget)
        self.AngleBar.setGeometry(QtCore.QRect(1740, 440, 131, 361))
        self.AngleBar.setMinimum(0)
        self.AngleBar.setMaximum(628)
        self.AngleBar.setPageStep(10)
        self.AngleBar.setProperty("value", 628)
        self.AngleBar.setObjectName("AngleBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1700, 70, 141, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1700, 190, 41, 31))
        self.label_2.setObjectName("label_2")
        self.Dt_field = QtWidgets.QLineEdit(self.centralwidget)
        self.Dt_field.setGeometry(QtCore.QRect(1800, 180, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Dt_field.setFont(font)
        self.Dt_field.setObjectName("Dt_field")
        self.Lim_field = QtWidgets.QLineEdit(self.centralwidget)
        self.Lim_field.setGeometry(QtCore.QRect(1800, 250, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Lim_field.setFont(font)
        self.Lim_field.setObjectName("Lim_field")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1700, 260, 51, 31))
        self.label_3.setObjectName("label_3")
        self.SpaceWidget = SpaceWidget(self.centralwidget)
        self.SpaceWidget.setGeometry(QtCore.QRect(9, 10, 1681, 961))
        self.SpaceWidget.setObjectName("SpaceWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Planet System"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.LoadButton.setText(_translate("MainWindow", "Load"))
        self.Filename_field.setText(_translate("MainWindow", "Universe"))
        self.label.setText(_translate("MainWindow", "Filename:"))
        self.label_2.setText(_translate("MainWindow", "Dt:"))
        self.Dt_field.setText(_translate("MainWindow", "0.01"))
        self.Lim_field.setText(_translate("MainWindow", "100"))
        self.label_3.setText(_translate("MainWindow", "Lim:"))
from spacewidget import SpaceWidget