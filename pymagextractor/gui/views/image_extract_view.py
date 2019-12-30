'''
Initialize what's needed in the gui widget for the Extract window.

Azu note:
Any code change is not needed here.
To modify any looks to the Extract window GUI, please edit extract_controller.py
To modify any words for the wigets in Extract window GUI, please edit extract.py
'''

from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.gui.qt_windows.image_extraction import Ui_MainWindow
from PySide2.QtWidgets import QStyle
import pymagextractor.gui.views.widgets.video_render as CustomWidget
from pymagextractor.gui.views.widgets.bounding_boxes_viewer import BoundingBoxesViewer


class ImageExtractView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ImageExtractView, self).__init__()
        self.controller = controller
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.play_bnt.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.widget = QtWidgets.QWidget()
        # self.ui.scroll_area.setWidget(self.widget)
        self.layout_SArea = QtWidgets.QVBoxLayout(self.widget)

        self.image_viewer = CustomWidget.VideoRender(self)
        self.original_layout = QtWidgets.QVBoxLayout()
        self.original_layout.addWidget(self.image_viewer)
        self.ui.image_viewer.setLayout(self.original_layout)

        # XXX: Got this manually...
        # Turns out, QScrollArea is in a Widget group??? Need to find out how to contained it...
        self.bb_viewer = BoundingBoxesViewer(self.ui.centralwidget)
        self.bb_viewer.setGeometry(QtCore.QRect(939, -1, 201, 701))

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
