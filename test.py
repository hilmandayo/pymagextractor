import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import cv2


class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        cap = cv2.VideoCapture('/home/thales/Downloads/DBH03.mp4')
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()
        self.show()

    def run(self):
        return self.app.exec_()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QtWidgets.QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())

