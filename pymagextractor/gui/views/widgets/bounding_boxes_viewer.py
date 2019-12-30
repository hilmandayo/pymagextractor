from PySide2 import (QtCore as qtc,
                     QtGui as qtg,
                     QtWidgets as qtw)
from pathlib import Path
import numpy as np
from functools import partial


# class ClickableQLabel(qtw.QLabel):
#     def __init__(self, *args, **kwargs):
#         try:
#             self._info = kwargs.pop("info")
#         except KeyError:
#             self._info = None

#         super().__init__(*args, **kwargs)


#     def mousePressEvent(self, event):
#         print(self._info)



class BoundingBoxesViewer(qtw.QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWidgetResizable(True)

        content_widget = qtw.QWidget()
        self.setWidget(content_widget)

        self._grid = qtw.QGridLayout(content_widget)
        self._row_idx = None

    def set_callback_func(self, func):
        self._callback_func = func

    def add_images_row(self, images, info_list, row=None):
        if len(images) != len(info_list):
            raise Exception("`images` must have the same length as `info_list`")

        for i, (image, info) in enumerate(zip(images, info_list)):
            self.add_image(image, info, i)

    def add_image(self, image, info, col):
        # np.ndarray -> QImage -> QPixmap -> QIcon
        # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        height, width = image.shape[:2]
        image = np.require(image, np.uint8, "C")
        image = qtg.QPixmap.fromImage(qtg.QImage(image, width, height, qtg.QImage.Format_RGB888))
        image = image.scaled(30, 30)

        # https://stackoverflow.com/questions/3137805/how-to-set-image-on-qpushbutton
        icon = qtg.QIcon(image)
        button = qtw.QPushButton()
        button.setIcon(icon)
        button.setIconSize(image.rect().size())
        button.setFixedSize(image.rect().size())

        button.clicked.connect(partial(self._callback_func, info["frame_id"][0]))

        if self._row_idx is None:
            self._row_idx = 0
        else:
            self._row_idx += 1

        self._grid.addWidget(button, self._row_idx, col)

    def set_images(self, row=0, col=0):
        for i, button in enumerate(self.buttons):
            self._grid.addWidget(button, i, 0)

    def return_info(self):
        print("return info")



if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    prog = BoundingBoxesViewer()


    def pr(val):
        print(val)

    prog.set_callback_func(pr)

    canvas = np.zeros([300, 300, 3], np.uint8)
    prog.add_image(canvas, {"frame_id": 1}, 0)
    prog.add_image(canvas, {"frame_id": 2}, 0)
    prog.show()

    sys.exit(app.exec_())
