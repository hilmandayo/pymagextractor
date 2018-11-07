import sys
import scipy.io as sio
from PyQt5 import QtGui, QtCore, QtWidgets
import cv2


class QtCapture(QtWidgets.QWidget):

    def __init__(self, filename):
        super(QtWidgets.QWidget, self).__init__()

        self.cap = cv2.VideoCapture('/home/thales/Downloads/DBH03.mp4')
        self.video_frame = QtWidgets.QLabel()
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.video_frame)
        self.setLayout(lay)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./30)

    def pause(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()


class ControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ControlWindow, self).__init__()
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("PyTrack")
        self.layout = QtWidgets.QVBoxLayout()

        self.capture = None

        self.matPosFileName = None
        self.videoFileName = None
        self.positionData = None
        self.updatedPositionData  = {'red_x':[], 'red_y':[], 'green_x':[], 'green_y': [], 'distance': []}
        self.updatedMatPosFileName = None

        self.isVideoFileLoaded = False
        self.isPositionFileLoaded = False

        self.quitAction = QtWidgets.QAction("&Exit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip('Close The App')
        self.quitAction.triggered.connect(self.closeApplication)

        self.openMatFile = QtWidgets.QAction("&Open Position File", self)
        self.openMatFile.setShortcut("Ctrl+Shift+T")
        self.openMatFile.setStatusTip('Open .mat File')
        self.openMatFile.triggered.connect(self.loadPosMatFile)

        self.openVideoFile = QtWidgets.QAction("&Open Video File", self)
        self.openVideoFile.setShortcut("Ctrl+Shift+V")
        self.openVideoFile.setStatusTip('Open .h264 File')
        self.openVideoFile.triggered.connect(self.loadVideoFile)

        self.mainMenu = self.menuBar()

        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openMatFile)
        self.fileMenu.addAction(self.openVideoFile)
        self.fileMenu.addAction(self.quitAction)

        self.imageCaptureWindow = QtWidgets.QWidget(self)
        self.start_button = QtWidgets.QPushButton('Start')
        self.layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.startCapture)
        self.start_button.setGeometry(0,10,40,30)
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.layout.addWidget(self.pause_button)
        self.pause_button.setGeometry(50,10,40,30)

        self.imageCaptureWindow.setLayout(self.layout)

        self.setCentralWidget(self.imageCaptureWindow)

        self.show()

    def startCapture(self):
        if not self.capture:
            self.capture = QtCapture(self.videoFileName)
            self.layout.addWidget(self.capture)
            self.pause_button.clicked.connect(self.capture.pause)
        self.capture.start()
        self.capture.show()

    def endCapture(self):
        self.capture.deleteLater()
        self.capture = None

    def loadPosMatFile(self):
        try:
            self.matPosFileName = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Select .mat position File'))
            self.positionData = sio.loadmat(self.matPosFileName)
            self.isPositionFileLoaded = True
        except:
            print("Please select a .mat file")

    def loadVideoFile(self):
        try:
            self.videoFileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Select .h264 Video File')
            self.isVideoFileLoaded = True
        except:
            print("Please select a .h264 file")

    def closeApplication(self):
        choice = QtWidgets.QMessageBox.question(self, 'Message','Do you really want to exit?',QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("Closing....")
            sys.exit()
        else:
            pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ControlWindow()
    sys.exit(app.exec_())