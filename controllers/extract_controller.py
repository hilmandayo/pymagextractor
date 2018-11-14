import sys
from PyQt5 import QtCore, QtGui, QtWidgets
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
        self.view.ui.slider.sliderMoved.connect(self.setPosition)
        self.view.mediaPlayer_original.positionChanged.connect(self.positionChanged)
        self.view.mediaPlayer_original.durationChanged.connect(self.durationChanged)

    def update(self):
        self.load_options()
        self.view.ui.frames_label.setText("0/"+str(self.home_controller.video.length_frames))

    def mediaStateChanged(self, state):
        if self.view.mediaPlayer_original.state() == QMediaPlayer.PlayingState:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPlay))

    def setPosition(self, position):
        self.view.mediaPlayer_original.setPosition(position)

    def positionChanged(self, position):
        self.view.ui.slider.setValue(position)
        self.view.ui.frames_label.setText(str(int(position*self.home_controller.video.fps/1000)) + "/" + str(self.home_controller.video.length_frames))

    def durationChanged(self, duration):
        self.view.ui.slider.setRange(0, duration)

    def run(self):
        self.view.mediaPlayer_original.setMedia(QMediaContent(QUrl.fromLocalFile(self.home_controller.video.path)))
        self.view.mediaPlayer_refined.setMedia(QMediaContent(QUrl.fromLocalFile(self.home_controller.video.path)))
        self.update()
        self.view.show()

    def play(self):
        if self.view.mediaPlayer_original.state() == QMediaPlayer.PlayingState:
            self.view.mediaPlayer_original.pause()
            self.view.mediaPlayer_refined.pause()
        else:
            self.view.mediaPlayer_original.play()
            self.view.mediaPlayer_refined.play()

    def load_options(self):
        for option_object in self.home_controller.optionsDB.object_list:
            group = QtWidgets.QGroupBox(option_object.name)
            vbox = QtWidgets.QVBoxLayout()
            for option_view in option_object.view_list:
                bnt = QtWidgets.QPushButton(option_view.name)
                vbox.addWidget(bnt)
            vbox.addStretch(1)
            group.setLayout(vbox)
            self.view.layout_SArea.addWidget(group)
