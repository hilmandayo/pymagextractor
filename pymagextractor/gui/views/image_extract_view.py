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

        # my button. only for tokutei object
        out = self.image_viewer.DHS["Tokutei Object"]
        temp_idx = None
        for kk, vv in out.handlers.items():
            if kk == "object":
                for i, ii in enumerate(vv.data):
                    button = QtWidgets.QPushButton(ii)
                    button.clicked.connect(self.button_clicked(kk, ii))
                    self.ui.button_grid.addWidget(button, 0, i)
            if kk == "view":
                for i, ii in enumerate(vv.data):
                    button = QtWidgets.QPushButton(ii)
                    button.clicked.connect(self.button_clicked(kk, ii))
                    self.ui.button_grid.addWidget(button, 1, i)

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

    def button_clicked(self, type_, subtype_):
        # determine frame id
        def clicked_func():
            curr = self.image_viewer.current_frame_number
            # will be only one
            objects = self.image_viewer.DHS["Tokutei Object"].get_objects("frame_id", curr)
            if objects:
                objects = [s for s in self.image_viewer.SAVED["Tokutei Object"] if s.track_id == objects][0]
                objects.save_on_button_click(curr, type_, subtype_)
            # determine existing object
            # update it
        return clicked_func
