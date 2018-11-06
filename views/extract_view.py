from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.extract import Ui_MainWindow
from PyQt5.QtWidgets import QStyle
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class ExtractView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ExtractView, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.play_bnt.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.mediaPlayer_original = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_original = QVideoWidget()

        self.mediaPlayer_refined = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_refined = QVideoWidget()

        self.ui.original_layout.addWidget(self.videoWidget_original)
        self.ui.refined_layout.addWidget(self.videoWidget_refined)

        self.mediaPlayer_original.setVideoOutput(self.videoWidget_original)
        self.mediaPlayer_refined.setVideoOutput(self.videoWidget_refined)
