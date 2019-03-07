from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.frontend.qt_windows.extract import Ui_MainWindow
from PySide2.QtWidgets import QStyle
import pymagextractor.frontend.views.widgets.video_render as CustomWidget


class ExtractView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ExtractView, self).__init__()
        self.controller = controller
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.play_bnt.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.widget = QtWidgets.QWidget()
        self.ui.scroll_area.setWidget(self.widget)
        self.layout_SArea = QtWidgets.QVBoxLayout(self.widget)

        self.refined_video = CustomWidget.VideoRender(self)
        self.refined_layout = QtWidgets.QVBoxLayout()
        self.refined_layout.addWidget(self.refined_video)
        self.ui.refined_box.setLayout(self.refined_layout)

        self.original_video = CustomWidget.VideoRender(self)
        self.original_layout = QtWidgets.QVBoxLayout()
        self.original_layout.addWidget(self.original_video)
        self.ui.original_box.setLayout(self.original_layout)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_S:
            if not self.controller.video_thread.playing:
                self.controller.video_thread.next_frame()
        elif qKeyEvent.key() == QtCore.Qt.Key_A:
            if not self.controller.video_thread.playing:
                self.controller.video_thread.previous_frame()
        elif qKeyEvent.key() == QtCore.Qt.Key_Z:
            self.controller.play()
        else:
            super().keyPressEvent(qKeyEvent)