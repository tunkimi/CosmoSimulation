# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateSystem.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(758, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LoadButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoadButton.setGeometry(QtCore.QRect(10, 10, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.LoadButton.setFont(font)
        self.LoadButton.setObjectName("LoadButton")
        self.AddPlanetButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddPlanetButton.setGeometry(QtCore.QRect(10, 601, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.AddPlanetButton.setFont(font)
        self.AddPlanetButton.setObjectName("AddPlanetButton")
        self.RemovePlanetButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemovePlanetButton.setGeometry(QtCore.QRect(160, 601, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.RemovePlanetButton.setFont(font)
        self.RemovePlanetButton.setObjectName("RemovePlanetButton")
        self.AddRockettButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddRockettButton.setGeometry(QtCore.QRect(10, 650, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.AddRockettButton.setFont(font)
        self.AddRockettButton.setObjectName("AddRockettButton")
        self.RemoveRocketButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveRocketButton.setGeometry(QtCore.QRect(160, 650, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.RemoveRocketButton.setFont(font)
        self.RemoveRocketButton.setObjectName("RemoveRocketButton")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(320, 10, 431, 631))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.TextFRocket = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextFRocket.setObjectName("TextFRocket")
        self.gridLayout.addWidget(self.TextFRocket, 7, 0, 1, 1)
        self.FRocketlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.FRocketlabel.setObjectName("FRocketlabel")
        self.gridLayout.addWidget(self.FRocketlabel, 6, 0, 1, 1)
        self.color1label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.color1label.setObjectName("color1label")
        self.gridLayout.addWidget(self.color1label, 2, 0, 1, 1)
        self.XYlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.XYlabel.setObjectName("XYlabel")
        self.gridLayout.addWidget(self.XYlabel, 0, 0, 1, 1)
        self.TextXY = QtWidgets.QTextEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.TextXY.setFont(font)
        self.TextXY.setObjectName("TextXY")
        self.gridLayout.addWidget(self.TextXY, 1, 0, 1, 1)
        self.color2label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.color2label.setObjectName("color2label")
        self.gridLayout.addWidget(self.color2label, 2, 1, 1, 1)
        self.Masslabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Masslabel.setObjectName("Masslabel")
        self.gridLayout.addWidget(self.Masslabel, 4, 0, 1, 1)
        self.TextMainColor = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextMainColor.setObjectName("TextMainColor")
        self.gridLayout.addWidget(self.TextMainColor, 3, 0, 1, 1)
        self.Vxylabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Vxylabel.setObjectName("Vxylabel")
        self.gridLayout.addWidget(self.Vxylabel, 0, 1, 1, 1)
        self.TextVxy = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextVxy.setObjectName("TextVxy")
        self.gridLayout.addWidget(self.TextVxy, 1, 1, 1, 1)
        self.TextSideColor = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextSideColor.setObjectName("TextSideColor")
        self.gridLayout.addWidget(self.TextSideColor, 3, 1, 1, 1)
        self.TextSize = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextSize.setObjectName("TextSize")
        self.gridLayout.addWidget(self.TextSize, 5, 1, 1, 1)
        self.Sizelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Sizelabel.setObjectName("Sizelabel")
        self.gridLayout.addWidget(self.Sizelabel, 4, 1, 1, 1)
        self.TextMass = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextMass.setObjectName("TextMass")
        self.gridLayout.addWidget(self.TextMass, 5, 0, 1, 1)
        self.ObhjectNamelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ObhjectNamelabel.setObjectName("ObhjectNamelabel")
        self.gridLayout.addWidget(self.ObhjectNamelabel, 6, 1, 1, 1)
        self.TextObjectName = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.TextObjectName.setObjectName("TextObjectName")
        self.gridLayout.addWidget(self.TextObjectName, 7, 1, 1, 1)
        self.CreateButton = QtWidgets.QPushButton(self.centralwidget)
        self.CreateButton.setGeometry(QtCore.QRect(540, 650, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.CreateButton.setFont(font)
        self.CreateButton.setObjectName("CreateButton")
        self.ApplyChangesButton = QtWidgets.QPushButton(self.centralwidget)
        self.ApplyChangesButton.setGeometry(QtCore.QRect(320, 650, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.ApplyChangesButton.setFont(font)
        self.ApplyChangesButton.setObjectName("ApplyChangesButton")
        self.ObjectList = QtWidgets.QListWidget(self.centralwidget)
        self.ObjectList.setGeometry(QtCore.QRect(10, 60, 291, 531))
        self.ObjectList.setObjectName("ObjectList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Space Creator"))
        self.LoadButton.setText(_translate("MainWindow", "Load"))
        self.AddPlanetButton.setText(_translate("MainWindow", "Add Planet"))
        self.RemovePlanetButton.setText(_translate("MainWindow", "Remove Planet"))
        self.AddRockettButton.setText(_translate("MainWindow", "Add Rocket"))
        self.RemoveRocketButton.setText(_translate("MainWindow", "Remove Rocket"))
        self.FRocketlabel.setText(_translate("MainWindow", "Fmax"))
        self.color1label.setText(_translate("MainWindow", "Main color"))
        self.XYlabel.setText(_translate("MainWindow", "Coordinates"))
        self.color2label.setText(_translate("MainWindow", "Side color"))
        self.Masslabel.setText(_translate("MainWindow", "Mass"))
        self.Vxylabel.setText(_translate("MainWindow", "Velocities"))
        self.Sizelabel.setText(_translate("MainWindow", "Size"))
        self.ObhjectNamelabel.setText(_translate("MainWindow", "Object name"))
        self.CreateButton.setText(_translate("MainWindow", "Create"))
        self.ApplyChangesButton.setText(_translate("MainWindow", "Apply changes"))