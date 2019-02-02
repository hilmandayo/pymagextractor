from PySide2 import QtCore, QtGui, QtWidgets
import pymagextractor.frontend.views.widgets.graphics_rect_item as CustomWidget


class VideoRender(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(VideoRender, self).__init__()
        self.main_window = parent
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.size_adjusted = False
        self.ratio = 1
        self.setAcceptDrops(True)

        # Config QGraphics objects
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        # Frame
        self.original_frame = None
        self.rescaled_frame = None
        self.scene_frame = QtWidgets.QGraphicsPixmapItem()

        # Current Detection Selection
        self.init_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()
        self.drawing = False
        self.current_selection = QtWidgets.QGraphicsRectItem()
        self.brush_current = QtGui.QBrush(QtGui.QColor(10, 10, 100, 120))

        # Detections
        self.detection = []
        self.detection_objects = []  # List of GraphicsRectItem objects
        self.brush_detection = QtGui.QBrush(QtGui.QColor(100, 10, 10, 120))

        self.init()

    def init(self):
        self.size_adjusted = False
        self.ratio = 1

    def set_frame(self, original_frame):
        """Set frame to be shown and resize the frame and widget"""
        self.original_frame = original_frame
        # Resize frame
        self.rescaled_frame = self.original_frame.scaled(self.size(), QtCore.Qt.KeepAspectRatio)

        # Adjust render widget dimensions depending on the video
        if not self.size_adjusted:
            self.ratio = self.rescaled_frame.size().height() / self.original_frame.size().height()
            self.resize(self.rescaled_frame.size())
            self.size_adjusted = True

        self.update_frame()

    def update_frame(self):
        """"Update the frame and all the detection squares"""
        self.scene.clear()
        # Display image/frame
        if self.rescaled_frame:
            self.scene_frame = QtWidgets.QGraphicsPixmapItem(self.rescaled_frame)
            self.scene.addItem(self.scene_frame)
            self.fitInView(self.scene_frame)
        # Draw new detection square
        if self.drawing:
            self.current_selection = QtWidgets.QGraphicsRectItem(QtCore.QRect(self.init_point, self.end_point))
            self.current_selection.setBrush(self.brush_current)
            self.scene.addItem(self.current_selection)
        # Detect all objects according to the Track List
        self.detection_objects = []
        for element in self.detection:
            d = CustomWidget.GraphicsRectItem(element.rect(self.ratio))
            d.setBrush(self.brush_detection)
            d.set_edit_mode(self.main_window.controller.edit_mode)
            self.scene.addItem(d)
            self.detection_objects.append(d)

    def set_detection_list(self, set_of_elements):
        """Set the position of all the recognition squares"""
        self.detection = set_of_elements

    def save_frame_selection(self):
        """Crop frame and save in a file"""
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, type = QtWidgets.QFileDialog.getSaveFileName(self.main_window, "QFileDialog.getSaveFileName()", "",
                                                                ".jpg;;.png", options=options)

        self.original_frame.copy(QtCore.QRect(self.init_point/self.ratio, self.end_point/self.ratio)).save(file_name + type)

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
        # Save selection into a image
        if not self.main_window.controller.edit_mode:
            menu = QtWidgets.QMenu(self)
            save_action = menu.addAction("Save")
            menu.addAction(save_action)
            action = menu.exec_(QtGui.QCursor.pos())
            if action == save_action:
                self.save_frame_selection()
            self.drawing = False
            self.update_frame()

    def enterEvent(self, event):
        if not self.main_window.controller.edit_mode:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        return super(VideoRender, self).enterEvent(event)

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        return super(VideoRender, self).enterEvent(event)
