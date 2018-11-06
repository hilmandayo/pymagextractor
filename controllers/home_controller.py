import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.home_view import HomeView
from controllers.display_controller import DisplayController
from controllers.extract_controller import ExtractController
from controllers.object_controller import ObjectController
from models.video import Video


class HomeController:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        # List of models
        self.video = Video()
        self.list_objects = []

        self.view = HomeView(self)

        # List of controllers
        self.display_controller = DisplayController(self)
        self.extractor_controller = ExtractController(self)
        self.object_controller = ObjectController(self)

        self.init()

    def init(self):
        self.view.ui.search_bnt.clicked.connect(self.search_video)
        self.view.ui.start_bnt.clicked.connect(self.start)
        self.view.ui.add_bnt.clicked.connect(self.add_object)
        self.update_video_browser(self.view.ui.video_browser)
        self.view.ui.object_list.clicked.connect(self.on_listview)

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

        self.update_video_browser(self.view.ui.video_browser)

    def start(self):
        self.extractor_controller.run()

    def update_video_browser(self, label):
        if self.video.path:
            label.setText(self.video.path)
            self.view.ui.start_bnt.setEnabled(True)
        else:
            label.setText("Select a video")

    def add_object(self):
        self.object_controller.run()

    def update_object_list(self):
        self.view.ui.object_list.clear()
        for object in self.list_objects:
            self.view.ui.object_list.addItem(object.name)

    def on_listview(self, index):
        self.object_controller.run(self.list_objects[index.row()])
        print(index.data())

