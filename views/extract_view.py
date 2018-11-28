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

        self.refined_video = VideoRender("Refined Video")
        self.refined_layout = QtWidgets.QVBoxLayout()
        self.refined_layout.addWidget(self.refined_video)
        self.ui.refined_box.setLayout(self.refined_layout)


class VideoRender(QtWidgets.QLabel):

    def __init__(self, text):
        super(VideoRender, self).__init__()
        self.setGeometry(0, 0, 410, 310)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setText(text)
        self.frame = None
        self.size = self.size()
        self.ratio = 1
        self.init_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def set_frame(self, original_frame):
        # Resize frame
        self.frame = original_frame.scaled(self.size, QtCore.Qt.KeepAspectRatio)
        self.ratio = original_frame.size().width()/self.frame.size().width()
        self.resize(self.frame.size())
        self.update()

    def paintEvent(self, event):
        frame_painter = QtGui.QPainter()
        frame_painter.begin(self)
        if self.frame:
            frame_painter.drawPixmap(0, 0, self.frame)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        frame_painter.setBrush(br)
        frame_painter.drawRect(QtCore.QRect(self.init_point, self.end_point))
        frame_painter.end()

    def mousePressEvent(self, event):
        print("Oi")
        self.init_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.init_point = event.pos()
        self.end_point = event.pos()
        self.update()
