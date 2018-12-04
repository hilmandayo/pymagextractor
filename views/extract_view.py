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

        self.refined_video = VideoRender()
        self.refined_layout = QtWidgets.QVBoxLayout()
        self.refined_layout.addWidget(self.refined_video)
        self.ui.refined_box.setLayout(self.refined_layout)

        self.original_video = VideoRender()
        self.original_layout = QtWidgets.QVBoxLayout()
        self.original_layout.addWidget(self.original_video)
        self.ui.original_box.setLayout(self.original_layout)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_S:
            if not self.controller.video_thread.playing:
                self.controller.video_thread.next_frame_slot()
        elif qKeyEvent.key() == QtCore.Qt.Key_A:
            if not self.controller.video_thread.playing:
                self.controller.video_thread.previous_frame_slot()
        elif qKeyEvent.key() == QtCore.Qt.Key_Z:
            self.controller.play()
        else:
            super().keyPressEvent(qKeyEvent)


class VideoRender(QtWidgets.QLabel):

    def __init__(self):
        super(VideoRender, self).__init__()
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.frame = None
        self.recognition = [[20,10,60,20], [90,100,100,150]]
        self.ratio = 1
        self.init_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()
        self.drawing = False
        self.size_adjusted = False

    def init(self):
        self.size_adjusted = False

    def set_frame(self, original_frame):
        # Resize frame
        self.frame = original_frame.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        if not self.size_adjusted:
            self.ratio = original_frame.size().width() / self.frame.size().width()
            self.resize(self.frame.size())
            self.size_adjusted = True
        self.update()

    def set_recognition(self, set_of_elements):
        self.recognition = set_of_elements

    def paintEvent(self, event):
        frame_painter = QtGui.QPainter()
        frame_painter.begin(self)
        # Draw frame
        if self.frame:
            frame_painter.drawPixmap(0, 0, self.frame)
        # Draw new recognition square
        if self.drawing:
            br = QtGui.QBrush(QtGui.QColor(10, 10, 100, 120))
            frame_painter.setBrush(br)
            frame_painter.drawRect(QtCore.QRect(self.init_point, self.end_point))
        # Draw recognitions on the CSV file loaded
        for element in self.recognition:
            br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 120))
            frame_painter.setBrush(br)
            frame_painter.drawRect(QtCore.QRect(QtCore.QPoint(element[0], element[1]), QtCore.QPoint(element[2], element[3])))
        frame_painter.end()

    def mousePressEvent(self, event):
        self.drawing = True
        self.init_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if x < 0:
            self.end_point.setX(0)
        elif x > self.size().width():
            self.end_point.setX(self.size().width()-4)
        else:
            self.end_point.setX(x)
        if y < 0:
            self.end_point.setY(0)
        elif y > self.size().height():
            self.end_point.setY(self.size().height()-4)
        else:
            self.end_point.setY(y)
        self.update()

    def mouseReleaseEvent(self, event):
        menu = QtWidgets.QMenu(self)
        save_action = menu.addAction("Save")
        menu.addAction(save_action)
        menu.exec_(QtGui.QCursor.pos())
        self.drawing = False
        self.update()

    def enterEvent(self, event):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        return super(VideoRender, self).enterEvent(event)

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        return super(VideoRender, self).enterEvent(event)
