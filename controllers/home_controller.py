import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.home_view import HomeView
from controllers.display_controller import DisplayController
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
        self.display_controller = DisplayController(self)
        self.extractor_controller = ExtractController(self)
        self.object_controller = ObjectController(self)

        self.init()
        self.update()

    def init(self):
        self.view.ui.search_bnt.clicked.connect(self.search_video)
        self.view.ui.start_bnt.clicked.connect(self.start)
        self.view.ui.add_bnt.clicked.connect(self.add_object)
        self.view.ui.object_list.clicked.connect(self.on_listview)
        self.view.ui.save_bnt.clicked.connect(self.save_options)
        self.view.ui.load_bnt.clicked.connect(self.load_options)

    def update(self):
        self.update_object_list()
        self.update_video_browser()

    def run(self):
        self.view.show()
        return self.app.exec_()

    def search_video(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            self.video.path = file_path

        self.update()

    def start(self):
        self.extractor_controller.run()

    def update_video_browser(self):
        if self.video.path:
            self.view.ui.video_browser.setText(self.video.path)
            self.view.ui.start_bnt.setEnabled(True)

    def add_object(self):
        self.object_controller.run()

    def update_object_list(self):
        self.view.ui.object_list.clear()
        for object in self.optionsDB.object_list:
            self.view.ui.object_list.addItem(object.name)

    def on_listview(self, index):
        self.object_controller.run(self.optionsDB.object_list[index.row()])

    def save_options(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self.view, "QFileDialog.getSaveFileName()", "",
                                                            "XML files (*.xml)", options=options)
        if file_name:
            if not (".xml" in file_name):
                file_name += ".xml"
            self.optionsDB.save_db(file_name)

    def load_options(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "XML files (*.xml)", options=options)
        if file_path:
            self.optionsDB.load_db(file_path)

        self.update()


