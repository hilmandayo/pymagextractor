import sys
from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.gui.views.object_view import ObjectView
from pymagextractor.models.container.object import Object
from pymagextractor.gui.controllers.view_controller import ViewController


class ObjectController:

    def __init__(self, home_controller):
        # Controllers and Views
        self.home_controller = home_controller
        self.view_controller = ViewController(self)
        self.view = ObjectView(self)

        self.new_object = None
        self.edit_object = None
        self.init()

    def init(self):
        """Initial setup for connecting all events"""
        self.view.ui.cancel_bnt.clicked.connect(self.close)
        self.view.ui.save_bnt.clicked.connect(self.save)
        self.view.ui.delete_bnt.clicked.connect(self.delete)
        self.view.ui.add_view_bnt.clicked.connect(self.add_view)
        self.view.ui.object_name.textChanged.connect(self.update_name)
        self.view.ui.view_list.clicked.connect(self.on_listview)

    def update(self):
        """Update for every time the controller is called"""
        self.view.ui.object_name.setText(self.new_object.name)
        self.update_view_list()
        # If it's editing mode
        if self.edit_object:
            self.view.ui.delete_bnt.setEnabled(True)
        else:
            self.view.ui.delete_bnt.setEnabled(False)

    def run(self, object_selected=None):
        """Start window"""
        self.new_object = Object()
        self.edit_object = object_selected
        if self.edit_object:
            self.new_object.name = self.edit_object.name
            self.new_object.view_list = self.edit_object.view_list

        self.update()
        self.view.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view.show()

    def close(self):
        """Close window"""
        self.home_controller.update()
        self.view.close()

    def save(self):
        """Save new object"""
        if self.new_object.verify():
            # If it's editing a new object delete the old one and add the new one
            if self.edit_object:
                self.home_controller.optionsDB.delete_object(self.edit_object)

            if self.home_controller.optionsDB.add_object(self.new_object):
                QtWidgets.QMessageBox.about(self.view, "Success", "Object Saved")
                self.home_controller.update()
                self.view.close()
            else:
                self.home_controller.optionsDB.add_object(self.edit_object)  # Poor implementation
                QtWidgets.QMessageBox.about(self.view, "Error", "Name already exist")


        else:
            QtWidgets.QMessageBox.about(self.view, "Error", "Information Incomplete")

    def delete(self):
        """Deleting the editing object"""
        self.home_controller.optionsDB.delete_object(self.edit_object)
        QtWidgets.QMessageBox.about(self.view, "Success", "Object Deleted")
        self.home_controller.update()
        self.view.close()

    def update_name(self):
        self.new_object.name = self.view.ui.object_name.text()

    def add_view(self):
        """Call new window to add a new view to the object"""
        self.view_controller.run(self.new_object)

    def update_view_list(self):
        self.view.ui.view_list.clear()
        for view in self.new_object.view_list:
            self.view.ui.view_list.addItem(view.name)

    def on_listview(self, index):
        self.view_controller.run(self.new_object, self.new_object.view_list[index.row()])
