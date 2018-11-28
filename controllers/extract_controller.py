from PySide2 import QtCore, QtGui, QtWidgets
from views.extract_view import ExtractView
from PySide2.QtWidgets import QStyle
import cv2, time


class ExtractController(QtCore.QObject):

    def __init__(self, home_controller):
        super(ExtractController, self).__init__()
        self.home_controller = home_controller
        self.video_widget = VideoThread(self)
        self.view = ExtractView(self)
        self.init()

    def init(self):
        self.view.ui.play_bnt.clicked.connect(self.play)
        self.view.ui.slider.sliderPressed.connect(self.video_widget.pause)
        self.view.ui.slider.sliderReleased.connect(self.set_frame)
        self.video_widget.changePixmap.connect(self.load_video)
        self.video_widget.changeState.connect(self.update_button)

    def update(self):
        self.load_options()
        self.view.ui.frames_label.setText("0/"+str(self.home_controller.video.length_frames))
        self.view.ui.slider.setRange(0, self.home_controller.video.length_frames)

    @QtCore.Slot(QtGui.QImage, int)
    def load_video(self, image, frame_number):
        # Change ratio size of the image according to the label's size
        original_image = image.scaled(self.view.ui.original_video.width(),
                                      self.view.ui.original_video.height(), QtCore.Qt.KeepAspectRatio)

        # Update number of frame
        self.update_frame_count(frame_number)
        self.slider_update(frame_number)
        self.view.ui.original_video.setPixmap(QtGui.QPixmap.fromImage(original_image))
        self.view.refined_video.set_frame(QtGui.QPixmap.fromImage(image))

    @QtCore.Slot(bool)
    def update_button(self, playing):
        if playing:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPlay))

    def set_frame(self):
        self.video_widget.jump_frame_slot(self.view.ui.slider.value())

    def slider_update(self, position):
        self.view.ui.slider.setValue(position)

    def update_frame_count(self, frame_number):
        self.view.ui.frames_label.setText(str(frame_number) + "/" +
                                          str(self.home_controller.video.length_frames))

    def run(self):
        self.video_widget.set_video(self.home_controller.video)
        self.video_widget.start()
        self.update()
        self.view.show()

    def play(self):
        if self.video_widget.playing:
            self.video_widget.pause()
        else:
            self.video_widget.play()

    def load_options(self):
        # Clear Scroll Area (Options Area)
        for i in reversed(range(self.view.layout_SArea.count())):
            self.view.layout_SArea.itemAt(i).widget().deleteLater()
        # Add objects for the Scroll Area (Option Area)
        for option_object in self.home_controller.optionsDB.object_list:
            group = QtWidgets.QGroupBox(option_object.name)
            vbox = QtWidgets.QVBoxLayout()
            for option_view in option_object.view_list:
                bnt = QtWidgets.QPushButton(option_view.name)
                vbox.addWidget(bnt)
            vbox.addStretch(1)
            group.setLayout(vbox)
            self.view.layout_SArea.addWidget(group)


class VideoThread(QtCore.QThread):
    changePixmap = QtCore.Signal(QtGui.QImage, int)
    changeState = QtCore.Signal(bool)

    def __init__(self, video=None):
        super(VideoThread, self).__init__()
        self.video = video
        self.playing = False
        self.current_frame = 0

    def set_video(self, video):
        self.video = video

    def next_frame_slot(self):
        ret, frame = self.video.cv.read()
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                             QtGui.QImage.Format_RGB888)
            self.current_frame = self.video.cv.get(cv2.CAP_PROP_POS_FRAMES)
            self.changePixmap.emit(image, self.current_frame)

    def jump_frame_slot(self, frame_slot):
        self.video.cv.set(cv2.CAP_PROP_POS_FRAMES, frame_slot)
        self.next_frame_slot()

    def previous_frame_slot(self):
        if self.current_frame > 0:
            self.current_frame -= 2
        self.jump_frame_slot(self.current_frame)

    def play(self):
        self.playing = True
        self.changeState.emit(self.playing)

    def run(self):
        while True:
            while self.playing:
                self.next_frame_slot()
                time.sleep(1/self.video.fps)
            time.sleep(0.1)

    def pause(self):
        self.playing = False
        self.changeState.emit(self.playing)