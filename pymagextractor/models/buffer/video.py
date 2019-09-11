"""Module containing the `Video` class."""


from PySide2 import QtGui
from pymagextractor.models.buffer.buffermaster import BufferMaster
from pymagextractor.models.buffer.frame import Frame
import ctypes as ctypes
import cv2


class Video(BufferMaster):
    def __init__(self, *args, **kwargs):
        # TODO: Documents the args and kwargs.
        super().__init__(*args, **kwargs)

    def next_frame_slot(self):
        # xfce4-taskmanager
        # ret, frame = self._buffer.read()
        image_cv = self.read(rgb=True)
        # TODO: Implement an algorithm to handle a thread version of images list.
        frame = QtGui.QImage(image_cv.data, image_cv.shape[1], image_cv.shape[0],
                                QtGui.QImage.Format_RGB888)

        # Fixing memory leak bug at Pyside QImage constructor
        ctypes.c_long.from_address(id(image_cv)).value = 1
        return Frame(self.current_frame_id, QtGui.QPixmap.fromImage(frame))

    def jump_frame_slot(self, frame_slot):
        self._buffer.set(cv2.CAP_PROP_POS_FRAMES, frame_slot - 1)
        return self.next_frame_slot()

    def previous_frame_slot(self):
        if self.current_frame_id > 0:
            return self.jump_frame_slot(self.current_frame_id - 2)
        else:
            return self.jump_frame_slot(self.current_frame_id)

    @property
    def frames_sequence(self):
        return list(range(1, self.n_frames))


# This is the previous class.
# Let it here for possible future references.
class _Video:

    def __init__(self):
        self.path = ""
        self.cv = None
        self.fps = 30  # Normally 30 frames per second
        self.length_frames = 0
        self.duration = 0
        self.width = 0
        self.height = 0

    def set_path(self, path):
        self.path = path
        self.cv = cv2.VideoCapture(self.path)
        self.fps = self.cv.get(cv2.CAP_PROP_FPS)
        self.length_frames = int(self.cv.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.cv.get(cv2.CAP_PROP_POS_MSEC)
        self.width = self.cv.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cv.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def frame_size(self):
        return self.width, self.height

    def frames_sequence(self):
        return list(range(1, self.length_frames))

    def current_frame_id(self):
        return self.cv.get(cv2.CAP_PROP_POS_FRAMES)

    def next_frame_slot(self):
        # xfce4-taskmanager
        ret, frame = self.cv.read()
        if ret:
            image_cv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = QtGui.QImage(image_cv.data, image_cv.shape[1], image_cv.shape[0],
                                  QtGui.QImage.Format_RGB888)

            # Fixing memory leak bug at Pyside QImage constructor
            ctypes.c_long.from_address(id(image_cv)).value = 1
            return Frame(self.current_frame_id(), QtGui.QPixmap.fromImage(frame))

    def jump_frame_slot(self, frame_slot):
        self.cv.set(cv2.CAP_PROP_POS_FRAMES, frame_slot - 1)
        return self.next_frame_slot()

    def previous_frame_slot(self):
        if self.current_frame_id() > 0:
            return self.jump_frame_slot(self.current_frame_id() - 2)
        else:
            return self.jump_frame_slot(self.current_frame_id())
