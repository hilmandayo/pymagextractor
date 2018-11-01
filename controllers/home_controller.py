import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from views.home_view import HomeView
from controllers.display_controller import DisplayController
from models.video import Video


class HomeController:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = HomeView(self)
        self.video = Video()
        self.display_controller = DisplayController(self)
        self.init()

    def init(self):
        self.view.ui.pushButton_load.clicked.connect(self.load_video)
        self.view.ui.pushButton_display.clicked.connect(self.display_video)
        self.update_video_label(self.view.ui.label_video)

    def run(self):
        self.view.show()
        return self.app.exec_()

    def load_video(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            self.video.path = file_path

        self.update_video_label(self.view.ui.label_video)

    def display_video(self):
        self.display_controller.run()

    def update_video_label(self, label):
        if self.video.path:
            label.setText("Video Info: " + self.video.path)
        else:
            label.setText("Video Info: No video loaded yet")
