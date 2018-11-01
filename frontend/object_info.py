# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/object_info.ui',
# licensing of 'frontend/object_info.ui' applies.
#
# Created: Fri Nov  2 03:13:55 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 242)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 90, 371, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.front_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.front_text.setReadOnly(True)
        self.front_text.setObjectName("front_text")
        self.horizontalLayout_2.addWidget(self.front_text)
        self.front_search_bnt = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.front_search_bnt.setObjectName("front_search_bnt")
        self.horizontalLayout_2.addWidget(self.front_search_bnt)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 140, 371, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.back_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.back_text.setReadOnly(True)
        self.back_text.setObjectName("back_text")
        self.horizontalLayout_3.addWidget(self.back_text)
        self.back_search_bnt = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.back_search_bnt.setObjectName("back_search_bnt")
        self.horizontalLayout_3.addWidget(self.back_search_bnt)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.name_text.setObjectName("name_text")
        self.horizontalLayout.addWidget(self.name_text)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(130, 10, 131, 17))
        self.label_4.setObjectName("label_4")
        self.save_bnt = QtWidgets.QPushButton(Form)
        self.save_bnt.setGeometry(QtCore.QRect(310, 200, 80, 25))
        self.save_bnt.setObjectName("save_bnt")
        self.cancel_bnt = QtWidgets.QPushButton(Form)
        self.cancel_bnt.setGeometry(QtCore.QRect(20, 200, 80, 25))
        self.cancel_bnt.setObjectName("cancel_bnt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Front:", None, -1))
        self.front_search_bnt.setText(QtWidgets.QApplication.translate("Form", "Search", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Back:", None, -1))
        self.back_search_bnt.setText(QtWidgets.QApplication.translate("Form", "Search", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Object Name:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Object Information", None, -1))
        self.save_bnt.setText(QtWidgets.QApplication.translate("Form", "Save", None, -1))
        self.cancel_bnt.setText(QtWidgets.QApplication.translate("Form", "Cancel", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

