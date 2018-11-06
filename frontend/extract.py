# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/extract.ui',
# licensing of 'frontend/extract.ui' applies.
#
# Created: Fri Nov  2 05:28:57 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(993, 511)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 821, 471))
        self.groupBox.setObjectName("groupBox")
        self.original_box = QtWidgets.QGroupBox(self.groupBox)
        self.original_box.setGeometry(QtCore.QRect(10, 30, 391, 331))
        self.original_box.setObjectName("original_box")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.original_box)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 29, 371, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.original_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.original_layout.setContentsMargins(0, 0, 0, 0)
        self.original_layout.setObjectName("original_layout")
        self.refined_box = QtWidgets.QGroupBox(self.groupBox)
        self.refined_box.setGeometry(QtCore.QRect(410, 30, 391, 331))
        self.refined_box.setObjectName("refined_box")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.refined_box)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 371, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.refined_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.refined_layout.setContentsMargins(0, 0, 0, 0)
        self.refined_layout.setObjectName("refined_layout")
        self.play_bnt = QtWidgets.QPushButton(self.groupBox)
        self.play_bnt.setGeometry(QtCore.QRect(370, 430, 80, 25))
        self.play_bnt.setText("")
        self.play_bnt.setObjectName("play_bnt")
        self.previous_bnt = QtWidgets.QPushButton(self.groupBox)
        self.previous_bnt.setGeometry(QtCore.QRect(270, 430, 80, 25))
        self.previous_bnt.setObjectName("previous_bnt")
        self.next_bnt = QtWidgets.QPushButton(self.groupBox)
        self.next_bnt.setGeometry(QtCore.QRect(470, 430, 80, 25))
        self.next_bnt.setObjectName("next_bnt")
        self.slider = QtWidgets.QSlider(self.groupBox)
        self.slider.setGeometry(QtCore.QRect(19, 400, 781, 20))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(380, 380, 54, 17))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 993, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.dockWidgetContents_2)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 10, 120, 321))
        self.groupBox_4.setObjectName("groupBox_4")
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Extractor", None, -1))
        self.original_box.setTitle(QtWidgets.QApplication.translate("MainWindow", "Original Detection", None, -1))
        self.refined_box.setTitle(QtWidgets.QApplication.translate("MainWindow", "Refined Detection", None, -1))
        self.previous_bnt.setText(QtWidgets.QApplication.translate("MainWindow", "Previous", None, -1))
        self.next_bnt.setText(QtWidgets.QApplication.translate("MainWindow", "Next", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Frames", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("MainWindow", "Save Options", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

