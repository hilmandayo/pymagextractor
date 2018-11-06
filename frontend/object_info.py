# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/object_info.ui',
# licensing of 'frontend/object_info.ui' applies.
#
# Created: Tue Nov  6 23:48:10 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 391)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(388, 391))
        Form.setMaximumSize(QtCore.QSize(388, 391))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.object_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.object_name.setObjectName("object_name")
        self.horizontalLayout.addWidget(self.object_name)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(130, 10, 131, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.save_bnt = QtWidgets.QPushButton(Form)
        self.save_bnt.setGeometry(QtCore.QRect(300, 360, 80, 25))
        self.save_bnt.setObjectName("save_bnt")
        self.cancel_bnt = QtWidgets.QPushButton(Form)
        self.cancel_bnt.setGeometry(QtCore.QRect(20, 360, 80, 25))
        self.cancel_bnt.setObjectName("cancel_bnt")
        self.delete_bnt = QtWidgets.QPushButton(Form)
        self.delete_bnt.setEnabled(False)
        self.delete_bnt.setGeometry(QtCore.QRect(200, 360, 91, 25))
        self.delete_bnt.setObjectName("delete_bnt")
        self.add_view_bnt = QtWidgets.QPushButton(Form)
        self.add_view_bnt.setGeometry(QtCore.QRect(290, 320, 91, 25))
        self.add_view_bnt.setObjectName("add_view_bnt")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(170, 80, 41, 17))
        self.label_5.setObjectName("label_5")
        self.view_list = QtWidgets.QListWidget(Form)
        self.view_list.setGeometry(QtCore.QRect(10, 100, 371, 211))
        self.view_list.setObjectName("view_list")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Object", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Object Name:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Object Information", None, -1))
        self.save_bnt.setText(QtWidgets.QApplication.translate("Form", "Save Object", None, -1))
        self.cancel_bnt.setText(QtWidgets.QApplication.translate("Form", "Cancel", None, -1))
        self.delete_bnt.setText(QtWidgets.QApplication.translate("Form", "Delete Object", None, -1))
        self.add_view_bnt.setText(QtWidgets.QApplication.translate("Form", "Add New View", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Views", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

