from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.frontend.qt_windows.extract import Ui_MainWindow
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
        """Set frame to be shown an resize the frame and view"""
        # Resize frame
        self.frame = original_frame.scaled(self.size(), QtCore.Qt.KeepAspectRatio)

        # Resize render widget
        if not self.size_adjusted:
            self.ratio = original_frame.size().width() / self.frame.size().width()
            self.resize(self.frame.size())
            self.size_adjusted = True

        self.update_frame()

    def update_frame(self):
        """"Update the frame and all the recognition squares"""
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
            recog = GraphicsRectItem(element[0], element[1], element[2], element[3])
            recog.setBrush(self.brush_detection)
            recog.set_edit_mode(self.main_window.controller.edit_mode)
            self.scene.addItem(recog)
            self.scene_recognition.append(recog)

    def set_recognition(self, set_of_elements):
        """Set the position of all the recognition squares"""
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
        if not self.main_window.controller.edit_mode:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        return super(VideoRender, self).enterEvent(event)

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        return super(VideoRender, self).enterEvent(event)


class GraphicsRectItem(QtWidgets.QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: QtCore.Qt.SizeFDiagCursor,
        handleTopMiddle: QtCore.Qt.SizeVerCursor,
        handleTopRight: QtCore.Qt.SizeBDiagCursor,
        handleMiddleLeft: QtCore.Qt.SizeHorCursor,
        handleMiddleRight: QtCore.Qt.SizeHorCursor,
        handleBottomLeft: QtCore.Qt.SizeBDiagCursor,
        handleBottomMiddle: QtCore.Qt.SizeVerCursor,
        handleBottomRight: QtCore.Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)

        self.edit_mode = False
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, self.edit_mode)
        self.updateHandlesPos()

    def set_edit_mode(self, edit):
        self.edit_mode = edit
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, self.edit_mode)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, self.edit_mode)
        self.update()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = QtCore.Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(QtCore.Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QtCore.QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QtCore.QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QtCore.QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QtCore.QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QtCore.QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QtCore.QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QtCore.QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QtGui.QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 100)))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1.0, QtCore.Qt.SolidLine))
        painter.drawRect(self.rect())

        if self.edit_mode:
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)))
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            for handle, rect in self.handles.items():
                if self.handleSelected is None or handle == self.handleSelected:
                    painter.drawEllipse(rect)
