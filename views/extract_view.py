from PySide2 import QtCore, QtGui, QtWidgets
from frontend.extract import Ui_MainWindow
from PySide2.QtWidgets import QStyle


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

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_S:
            if not self.controller.video_widget.playing:
                self.controller.video_widget.next_frame_slot()
        elif qKeyEvent.key() == QtCore.Qt.Key_A:
            if not self.controller.video_widget.playing:
                self.controller.video_widget.previous_frame_slot()
        elif qKeyEvent.key() == QtCore.Qt.Key_Z:
            self.controller.play()
        else:
            super().keyPressEvent(qKeyEvent)
