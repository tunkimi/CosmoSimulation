# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadSystem3var1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1781, 851))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SpaceWidget = SpaceWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(90)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SpaceWidget.sizePolicy().hasHeightForWidth())
        self.SpaceWidget.setSizePolicy(sizePolicy)
        self.SpaceWidget.setObjectName("SpaceWidget")
        self.horizontalLayout.addWidget(self.SpaceWidget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.LoadButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.LoadButton.setFont(font)
        self.LoadButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LoadButton.setObjectName("LoadButton")
        self.verticalLayout_4.addWidget(self.LoadButton)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.TextDt = QtWidgets.QTextEdit(self.widget)
        self.TextDt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextDt.setObjectName("TextDt")
        self.verticalLayout_4.addWidget(self.TextDt)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.TextTimeLimit = QtWidgets.QTextEdit(self.widget)
        self.TextTimeLimit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextTimeLimit.setObjectName("TextTimeLimit")
        self.verticalLayout_4.addWidget(self.TextTimeLimit)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.TextMoonNumber = QtWidgets.QTextEdit(self.widget)
        self.TextMoonNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextMoonNumber.setObjectName("TextMoonNumber")
        self.verticalLayout_4.addWidget(self.TextMoonNumber)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.TextMoonsR = QtWidgets.QTextEdit(self.widget)
        self.TextMoonsR.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextMoonsR.setObjectName("TextMoonsR")
        self.verticalLayout_4.addWidget(self.TextMoonsR)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.TextMoonsV = QtWidgets.QTextEdit(self.widget)
        self.TextMoonsV.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextMoonsV.setObjectName("TextMoonsV")
        self.verticalLayout_4.addWidget(self.TextMoonsV)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.TextEps = QtWidgets.QTextEdit(self.widget)
        self.TextEps.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TextEps.setObjectName("TextEps")
        self.verticalLayout_4.addWidget(self.TextEps)
        self.CheckR = QtWidgets.QCheckBox(self.widget)
        self.CheckR.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CheckR.setObjectName("CheckR")
        self.verticalLayout_4.addWidget(self.CheckR)
        self.CheckPhi = QtWidgets.QCheckBox(self.widget)
        self.CheckPhi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CheckPhi.setObjectName("CheckPhi")
        self.verticalLayout_4.addWidget(self.CheckPhi)
        self.CheckV = QtWidgets.QCheckBox(self.widget)
        self.CheckV.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CheckV.setObjectName("CheckV")
        self.verticalLayout_4.addWidget(self.CheckV)
        self.CheckShow = QtWidgets.QCheckBox(self.widget)
        self.CheckShow.setObjectName("CheckShow")
        self.verticalLayout_4.addWidget(self.CheckShow)
        self.StartButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.StartButton.setFont(font)
        self.StartButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.StartButton.setObjectName("StartButton")
        self.verticalLayout_4.addWidget(self.StartButton)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Planet System"))
        self.LoadButton.setText(_translate("MainWindow", "Load"))
        self.label.setText(_translate("MainWindow", "dt:"))
        self.TextDt.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.01</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Window limit"))
        self.TextTimeLimit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">20</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Moon number"))
        self.TextMoonNumber.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">24</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Moons R"))
        self.TextMoonsR.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">18</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Moons V"))
        self.TextMoonsV.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2.36</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Accuracy (%)"))
        self.TextEps.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.01</p></body></html>"))
        self.CheckR.setText(_translate("MainWindow", "R"))
        self.CheckPhi.setText(_translate("MainWindow", "Phi"))
        self.CheckV.setText(_translate("MainWindow", "V"))
        self.CheckShow.setText(_translate("MainWindow", "Show With Default"))
        self.StartButton.setText(_translate("MainWindow", "Start"))

from spacewidget import SpaceWidget
