import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.home_view import HomeView
from controllers.extract_controller import ExtractController
from controllers.object_controller import ObjectController
from models.video import Video
from models.optionsDB import OptionsDB


class HomeController:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        # List of models
        self.video = Video()
        self.optionsDB = OptionsDB()

        self.view = HomeView(self)

        # List of controllers
        self.extractor_controller = ExtractController(self)
        self.object_controller = ObjectController(self)

        self.init()
        self.update()

    def init(self):
        """Initial setup for connecting all events"""
        self.view.ui.search_bnt.clicked.connect(self.search_video)
        self.view.ui.start_bnt.clicked.connect(self.start)
        self.view.ui.add_bnt.clicked.connect(self.add_object)
        self.view.ui.object_list.clicked.connect(self.on_listview)
        self.view.ui.save_bnt.clicked.connect(self.save_options)
        self.view.ui.load_bnt.clicked.connect(self.load_options)

    def update(self):
        """Update for every time the controller is called"""
        self.update_object_list()
        self.update_video_browser()

    def run(self):
        """Start window"""
        self.view.show()
        return self.app.exec_()

    def search_video(self):
        """Find video path"""
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            self.video.set_path(file_path)

        self.update()

    def start(self):
        """Open video display window"""
        self.extractor_controller.run()

    def add_object(self):
        """Open add object window"""
        self.object_controller.run()

    def save_options(self):
        """Save objects on a xml file"""
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self.view, "QFileDialog.getSaveFileName()", "",
                                                            "XML files (*.xml)", options=options)
        if file_name:
            if not (".xml" in file_name):
                file_name += ".xml"
            self.optionsDB.save_db(file_name)

    def load_options(self):
        """Load a xml file to a list of objects"""
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "XML files (*.xml)", options=options)
        if file_path:
            self.optionsDB.load_db(file_path)
            print(file_path)

        self.update()

    def update_object_list(self):
        self.view.ui.object_list.clear()
        for object in self.optionsDB.object_list:
            self.view.ui.object_list.addItem(object.name)

    def update_video_browser(self):
        if self.video.path:
            self.view.ui.video_browser.setText(self.video.path)
            self.view.ui.start_bnt.setEnabled(True)

    def on_listview(self, index):
        self.object_controller.run(self.optionsDB.object_list[index.row()])




