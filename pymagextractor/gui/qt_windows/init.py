# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'init.ui',
# licensing of 'init.ui' applies.
#
# Created: Thu Nov 14 00:40:26 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DbPathSearchWindow(object):
    def setupUi(self, DbPathSearchWindow):
        DbPathSearchWindow.setObjectName("DbPathSearchWindow")
        DbPathSearchWindow.setEnabled(True)
        DbPathSearchWindow.resize(420, 110)
        DbPathSearchWindow.setMinimumSize(QtCore.QSize(420, 110))
        self.db_widget = QtWidgets.QWidget(DbPathSearchWindow)
        self.db_widget.setObjectName("db_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.db_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.db_grid = QtWidgets.QGridLayout()
        self.db_grid.setObjectName("db_grid")
        self.db_box_path = QtWidgets.QLineEdit(self.db_widget)
        self.db_box_path.setInputMask("")
        self.db_box_path.setText("")
        self.db_box_path.setObjectName("db_box_path")
        self.db_grid.addWidget(self.db_box_path, 0, 0, 1, 1)
        self.db_btn_search = QtWidgets.QPushButton(self.db_widget)
        self.db_btn_search.setObjectName("db_btn_search")
        self.db_grid.addWidget(self.db_btn_search, 0, 1, 1, 1)
        self.db_btn_generate = QtWidgets.QPushButton(self.db_widget)
        self.db_btn_generate.setEnabled(False)
        self.db_btn_generate.setObjectName("db_btn_generate")
        self.db_grid.addWidget(self.db_btn_generate, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.db_grid, 0, 1, 1, 1)
        DbPathSearchWindow.setCentralWidget(self.db_widget)

        self.retranslateUi(DbPathSearchWindow)
        QtCore.QMetaObject.connectSlotsByName(DbPathSearchWindow)

    def retranslateUi(self, DbPathSearchWindow):
        DbPathSearchWindow.setWindowTitle(QtWidgets.QApplication.translate("DbPathSearchWindow", "Pymagextractor", None, -1))
        self.db_box_path.setPlaceholderText(QtWidgets.QApplication.translate("DbPathSearchWindow", "/path/to/database", None, -1))
        self.db_btn_search.setText(QtWidgets.QApplication.translate("DbPathSearchWindow", "Search", None, -1))
        self.db_btn_generate.setText(QtWidgets.QApplication.translate("DbPathSearchWindow", "Generate", None, -1))

