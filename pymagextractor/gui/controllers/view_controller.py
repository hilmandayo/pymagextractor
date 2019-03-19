from PySide2 import QtCore, QtWidgets
from pymagextractor.gui.views.view_view import ViewView
from pymagextractor.models.container.object_view import ObjectView


class ViewController:

    def __init__(self, object_controller):
        # Controllers and views
        self.object_controller = object_controller
        self.view = ViewView(self)

        self.new_view = None
        self.edit_view = None
        self.init()

    def init(self):
        """Initial setup for connecting all events"""
        self.view.ui.cancel_bnt.clicked.connect(self.close)
        self.view.ui.save_bnt.clicked.connect(self.save)
        self.view.ui.delete_bnt.clicked.connect(self.delete)
        self.view.ui.view_search_bnt.clicked.connect(self.file_search)
        self.view.ui.view_name.textChanged.connect(self.update_name)

    def update(self):
        """Update for every time the controller is called"""
        self.view.ui.view_name.setText(self.new_view.name)
        self.view.ui.view_path.setText(self.new_view.path)
        # If it's editing mode
        if self.edit_view:
            self.view.ui.delete_bnt.setEnabled(True)
        else:
            self.view.ui.delete_bnt.setEnabled(False)

    def run(self, parent_object, view_selected=None):
        """Start window"""
        self.new_view = ObjectView(parent_object)
        self.edit_view = view_selected
        if self.edit_view:
            self.new_view.name = self.edit_view.name
            self.new_view.path = self.edit_view.path

        self.update()
        self.view.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view.show()

    def close(self):
        """Close window"""
        self.object_controller.update()
        self.view.close()

    def save(self):
        """Save new object"""
        self.new_view.name = self.view.ui.view_name.text()
        if self.new_view.verify():
            # If it's editing a new object delete the old one and add the new one
            if self.edit_view:
                self.object_controller.new_object.delete_view(self.edit_view)

            if self.object_controller.new_object.add_view(self.new_view):
                QtWidgets.QMessageBox.about(self.view, "Success", "View Saved")
                self.object_controller.update()
                self.view.close()
            else:
                self.object_controller.new_object.add_object(self.edit_view)  # Poor implementation
                QtWidgets.QMessageBox.about(self.view, "Error", "Name already exist")

        else:
            QtWidgets.QMessageBox.about(self.view, "Error", "Information Incomplete")

    def delete(self):
        """Deleting the editing object"""
        self.object_controller.new_object.delete_view(self.edit_view)
        QtWidgets.QMessageBox.about(self.view, "Success", "Object Deleted")
        self.object_controller.update()
        self.view.close()

    def update_name(self):
        self.new_view.name = self.view.ui.view_name.text()

    def file_search(self):
        """Look for a file at local folder"""
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            self.new_view.path = file_path

        self.update()
