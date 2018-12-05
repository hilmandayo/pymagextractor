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

        self.refined_video = VideoRender(self)
        self.refined_layout = QtWidgets.QVBoxLayout()
        self.refined_layout.addWidget(self.refined_video)
        self.ui.refined_box.setLayout(self.refined_layout)

        self.original_video = VideoRender(self)
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


class VideoRender(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(VideoRender, self).__init__()
        self.main_window = parent
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.size_adjusted = False
        self.ratio = 1
        self.setAcceptDrops(True)

        # Config QGraphics objects
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        # Frame
        self.frame = None
        self.scene_frame = QtWidgets.QGraphicsPixmapItem()

        # Current Detection Selection
        self.init_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()
        self.drawing = False
        self.current_selection = QtWidgets.QGraphicsRectItem()
        self.brush_current = QtGui.QBrush(QtGui.QColor(10, 10, 100, 120))

        # Detections
        self.recognition = [[20, 10, 60, 20], [90, 100, 100, 150]]
        self.scene_recognition = []
        self.brush_detection = QtGui.QBrush(QtGui.QColor(100, 10, 10, 120))

        self.init()

    def init(self):
        self.size_adjusted = False
        self.ratio = 1

    def set_frame(self, original_frame):
        # Resize frame
        self.frame = original_frame.scaled(self.size(), QtCore.Qt.KeepAspectRatio)

        # Resize render widget
        if not self.size_adjusted:
            self.ratio = original_frame.size().width() / self.frame.size().width()
            self.resize(self.frame.size())
            self.size_adjusted = True

        self.update_frame()

    def update_frame(self):
        self.scene.clear()
        # Display image/frame
        if self.frame:
            self.scene_frame = QtWidgets.QGraphicsPixmapItem(self.frame)
            self.scene.addItem(self.scene_frame)
            self.fitInView(self.scene_frame)
        # Draw new recognition square
        if self.drawing:
            self.current_selection = QtWidgets.QGraphicsRectItem(QtCore.QRect(self.init_point, self.end_point))
            self.current_selection.setBrush(self.brush_current)
            self.scene.addItem(self.current_selection)
        # Draw recognitions on the CSV file loaded
        self.scene_recognition = []
        for element in self.recognition:
            recog = QtWidgets.QGraphicsRectItem(element[0], element[1], element[2], element[3])
            recog.setBrush(self.brush_detection)
            recog.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.scene.addItem(recog)
            self.scene_recognition.append(recog)

    def set_recognition(self, set_of_elements):
        self.recognition = set_of_elements

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.main_window.controller.edit_mode:
            self.drawing = True
            self.init_point = event.pos()
            self.end_point = event.pos()
            self.update_frame()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.main_window.controller.edit_mode:
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
            self.update_frame()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if not self.main_window.controller.edit_mode:
            menu = QtWidgets.QMenu(self)
            save_action = menu.addAction("Save")
            menu.addAction(save_action)
            menu.exec_(QtGui.QCursor.pos())
            self.drawing = False
            self.update_frame()

    def enterEvent(self, event):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        return super(VideoRender, self).enterEvent(event)

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        return super(VideoRender, self).enterEvent(event)
