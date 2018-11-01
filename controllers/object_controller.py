import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.object_view import ObjectView
from models.object import Object


class ObjectController:

    def __init__(self, home_controller):
        self.home_controller = home_controller
        self.view = ObjectView(self)
        self.object = Object()
        self.init()

    def init(self):
        self.view.ui.cancel_bnt.clicked.connect(self.close)
        self.view.ui.save_bnt.clicked.connect(self.save)
        self.view.ui.front_search_bnt.clicked.connect(self.front_file_search)
        self.view.ui.back_search_bnt.clicked.connect(self.back_file_search)

    def run(self):
        self.view.show()

    def close(self):
        self.view.close()

    def save(self):
        self.object.name = self.view.ui.name_text.text()
        if self.object.verify():
            QtWidgets.QMessageBox.about(self.view, "Success", "Object Saved")
            self.view.close()
        else:
            QtWidgets.QMessageBox.about(self.view, "Error", "Information Incomplete")


    def file_search(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "All Files (*);;Python Files (*.py)", options=options)
        return file_path

    def front_file_search(self):
        file_path = self.file_search()
        if file_path:
            self.object.front = file_path
            self.view.ui.front_text.setText(file_path)

    def back_file_search(self):
        file_path = self.file_search()
        if file_path:
            self.object.back = file_path
            self.view.ui.back_text.setText(file_path)
