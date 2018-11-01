import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.home_view import HomeView
from controllers.display_controller import DisplayController
from controllers.object_controller import ObjectController
from models.video import Video


class HomeController:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = HomeView(self)
        self.video = Video()
        self.display_controller = DisplayController(self)
        self.object_controller = ObjectController(self)
        self.init()

    def init(self):
        self.view.ui.search_bnt.clicked.connect(self.search_video)
        self.view.ui.start_bnt.clicked.connect(self.display_video)
        self.view.ui.add_bnt.clicked.connect(self.add_object)
        self.update_video_browser(self.view.ui.video_browser)

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

    def display_video(self):
        self.display_controller.run()

    def update_video_browser(self, label):
        if self.video.path:
            label.setText(self.video.path)
        else:
            label.setText("Select a video")

    def add_object(self):
        self.object_controller.run()

