# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/new_view.ui',
# licensing of 'frontend/new_view.ui' applies.
#
# Created: Wed Nov  7 03:04:40 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 162)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(400, 162))
        Form.setMaximumSize(QtCore.QSize(400, 162))
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(170, 10, 41, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.view_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.view_name.setObjectName("view_name")
        self.horizontalLayout.addWidget(self.view_name)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 80, 371, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.view_path = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.view_path.setReadOnly(True)
        self.view_path.setObjectName("view_path")
        self.horizontalLayout_2.addWidget(self.view_path)
        self.view_search_bnt = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.view_search_bnt.setObjectName("view_search_bnt")
        self.horizontalLayout_2.addWidget(self.view_search_bnt)
        self.delete_bnt = QtWidgets.QPushButton(Form)
        self.delete_bnt.setEnabled(False)
        self.delete_bnt.setGeometry(QtCore.QRect(209, 130, 91, 25))
        self.delete_bnt.setObjectName("delete_bnt")
        self.save_bnt = QtWidgets.QPushButton(Form)
        self.save_bnt.setGeometry(QtCore.QRect(310, 130, 80, 25))
        self.save_bnt.setObjectName("save_bnt")
        self.cancel_bnt = QtWidgets.QPushButton(Form)
        self.cancel_bnt.setGeometry(QtCore.QRect(20, 130, 80, 25))
        self.cancel_bnt.setObjectName("cancel_bnt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "View", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "View", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "View Name:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "File:", None, -1))
        self.view_search_bnt.setText(QtWidgets.QApplication.translate("Form", "Search", None, -1))
        self.delete_bnt.setText(QtWidgets.QApplication.translate("Form", "Delete View", None, -1))
        self.save_bnt.setText(QtWidgets.QApplication.translate("Form", "Save View", None, -1))
        self.cancel_bnt.setText(QtWidgets.QApplication.translate("Form", "Cancel", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

