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
        self.edit_mode = False

    def init(self):
        self.view.ui.cancel_bnt.clicked.connect(self.close)
        self.view.ui.save_bnt.clicked.connect(self.save)
        self.view.ui.delete_bnt.clicked.connect(self.delete)
        self.view.ui.front_search_bnt.clicked.connect(self.front_file_search)
        self.view.ui.back_search_bnt.clicked.connect(self.back_file_search)

    def run(self, loaded_object=None):
        if loaded_object:
            self.object = loaded_object
            self.view.ui.name_text.setText(self.object.name)
            self.edit_mode = True
        else:
            self.object = Object()  # create a new object
            self.view.ui.name_text.setText("")
            self.edit_mode = False

        self.view.ui.delete_bnt.setEnabled(self.edit_mode)
        self.view.ui.save_bnt.setEnabled(not self.edit_mode)
        self.update_fields()
        self.view.show()

    def close(self):
        self.view.close()

    def save(self):
        self.object.name = self.view.ui.name_text.text()
        if self.object.verify():
            if self.edit_mode:
                QtWidgets.QMessageBox.about(self.view, "Success", "Alterations Saved")
            else:
                self.home_controller.list_objects.append(self.object)
                QtWidgets.QMessageBox.about(self.view, "Success", "New Object Saved")

            self.home_controller.update_object_list()
            self.view.close()
        else:
            QtWidgets.QMessageBox.about(self.view, "Error", "Information Incomplete")

    def delete(self):
        self.home_controller.list_objects.remove(self.object)
        QtWidgets.QMessageBox.about(self.view, "Error", "Object Deleted")
        self.home_controller.update_object_list()
        self.view.close()


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
            self.update_fields()

    def back_file_search(self):
        file_path = self.file_search()
        if file_path:
            self.object.back = file_path
            self.update_fields()

    def update_fields(self):
        self.view.ui.front_text.setText(self.object.front)
        self.view.ui.back_text.setText(self.object.back)
