import sys
from PySide2 import QtCore, QtGui, QtWidgets
from views.extract_view import ExtractView
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class ExtractController:

    def __init__(self, home_controller):
        self.home_controller = home_controller
        self.view = ExtractView(self)
        self.init()

    def init(self):
        self.view.ui.play_bnt.clicked.connect(self.play)
        self.view.mediaPlayer_original.stateChanged.connect(self.mediaStateChanged)
        self.view.mediaPlayer_refined.stateChanged.connect(self.mediaStateChanged)

    def mediaStateChanged(self, state):
        if self.view.mediaPlayer_original.state() == QMediaPlayer.PlayingState:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPlay))

    def run(self):
        self.view.mediaPlayer_original.setMedia(QMediaContent(QUrl.fromLocalFile(self.home_controller.video.path)))
        self.view.mediaPlayer_refined.setMedia(QMediaContent(QUrl.fromLocalFile(self.home_controller.video.path)))
        self.view.show()

    def play(self):
        if self.view.mediaPlayer_original.state() == QMediaPlayer.PlayingState:
            self.view.mediaPlayer_original.pause()
            self.view.mediaPlayer_refined.pause()
        else:
            self.view.mediaPlayer_original.play()
            self.view.mediaPlayer_refined.play()
