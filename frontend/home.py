# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        HomeWindow.setObjectName("HomeWindow")
        HomeWindow.resize(437, 203)
        self.centralwidget = QtWidgets.QWidget(HomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_display = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_display.setGeometry(QtCore.QRect(170, 80, 87, 29))
        self.pushButton_display.setObjectName("pushButton_display")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_about = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_about.setGeometry(QtCore.QRect(320, 80, 87, 29))
        self.pushButton_about.setObjectName("pushButton_about")
        self.pushButton_load = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load.setGeometry(QtCore.QRect(30, 80, 87, 29))
        self.pushButton_load.setObjectName("pushButton_load")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(20, 140, 401, 17))
        self.label_video.setObjectName("label_video")
        HomeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(HomeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 437, 23))
        self.menubar.setObjectName("menubar")
        HomeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(HomeWindow)
        self.statusbar.setObjectName("statusbar")
        HomeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(HomeWindow)
        QtCore.QMetaObject.connectSlotsByName(HomeWindow)

    def retranslateUi(self, HomeWindow):
        _translate = QtCore.QCoreApplication.translate
        HomeWindow.setWindowTitle(_translate("HomeWindow", "Pymagextractor"))
        self.pushButton_display.setText(_translate("HomeWindow", "Display Video"))
        self.label.setText(_translate("HomeWindow", "Menu"))
        self.pushButton_about.setText(_translate("HomeWindow", "About"))
        self.pushButton_load.setText(_translate("HomeWindow", "Load Video"))
        self.label_video.setText(_translate("HomeWindow", "Video Info"))

