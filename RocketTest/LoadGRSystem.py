# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadGRSystem.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1479, 720)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(1280, 660, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.StartButton.setFont(font)
        self.StartButton.setObjectName("StartButton")
        self.LoadButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadButton.setGeometry(QtCore.QRect(1280, 60, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.LoadButton.setFont(font)
        self.LoadButton.setObjectName("LoadButton")
        self.EngineBar = QtWidgets.QScrollBar(self.centralwidget)
        self.EngineBar.setGeometry(QtCore.QRect(1280, 280, 31, 371))
        self.EngineBar.setMaximum(100)
        self.EngineBar.setPageStep(8)
        self.EngineBar.setOrientation(QtCore.Qt.Vertical)
        self.EngineBar.setObjectName("EngineBar")
        self.AngleBar = QtWidgets.QDial(self.centralwidget)
        self.AngleBar.setGeometry(QtCore.QRect(1320, 280, 131, 371))
        self.AngleBar.setPageStep(10)
        self.AngleBar.setProperty("value", 50)
        self.AngleBar.setObjectName("AngleBar")
        self.Dt_field = QtWidgets.QTextEdit(self.centralwidget)
        self.Dt_field.setGeometry(QtCore.QRect(1280, 150, 181, 41))
        self.Dt_field.setObjectName("Dt_field")
        self.Lim_field = QtWidgets.QTextEdit(self.centralwidget)
        self.Lim_field.setGeometry(QtCore.QRect(1280, 230, 181, 41))
        self.Lim_field.setObjectName("Lim_field")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1280, 130, 181, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1280, 200, 181, 21))
        self.label_2.setObjectName("label_2")
        self.SpaceWidget = SpaceWidget(self.centralwidget)
        self.SpaceWidget.setGeometry(QtCore.QRect(10, 10, 871, 681))
        self.SpaceWidget.setObjectName("SpaceWidget")
        self.Load1Button = QtWidgets.QPushButton(self.centralwidget)
        self.Load1Button.setGeometry(QtCore.QRect(1280, 100, 91, 31))
        self.Load1Button.setObjectName("Load1Button")
        self.Load2Button = QtWidgets.QPushButton(self.centralwidget)
        self.Load2Button.setGeometry(QtCore.QRect(1380, 100, 81, 31))
        self.Load2Button.setObjectName("Load2Button")
        self.Filename_field = QtWidgets.QTextEdit(self.centralwidget)
        self.Filename_field.setGeometry(QtCore.QRect(1280, 10, 181, 41))
        self.Filename_field.setObjectName("Filename_field")
        self.Graph1Widget = GraphWidget(self.centralwidget)
        self.Graph1Widget.setGeometry(QtCore.QRect(900, 10, 371, 321))
        self.Graph1Widget.setObjectName("Graph1Widget")
        self.Graph1Widget_2 = GraphWidget(self.centralwidget)
        self.Graph1Widget_2.setGeometry(QtCore.QRect(900, 350, 371, 341))
        self.Graph1Widget_2.setObjectName("Graph1Widget_2")
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
        self.Dt_field.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.01</p></body></html>"))
        self.Lim_field.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">70</p></body></html>"))
        self.label.setText(_translate("MainWindow", "dt:"))
        self.label_2.setText(_translate("MainWindow", "Window limit"))
        self.Load1Button.setText(_translate("MainWindow", "Preset 1"))
        self.Load2Button.setText(_translate("MainWindow", "Preset 2"))
        self.Filename_field.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Universe</p></body></html>"))

from graphwidget import GraphWidget
from spacewidget import SpaceWidget
