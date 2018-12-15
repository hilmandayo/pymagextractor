from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.frontend.views.extract_view import ExtractView
from PySide2.QtWidgets import QStyle
import cv2, time
import ctypes as ctypes


class ExtractController(QtCore.QObject):

    def __init__(self, home_controller):
        super(ExtractController, self).__init__()
        self.home_controller = home_controller
        self.video_thread = VideoThread()
        self.view = ExtractView(self)
        self.video = self.home_controller.video

        # Modes
        self.edit_mode = False

        # Connect all signals
        self.view.ui.play_bnt.clicked.connect(self.play)
        self.view.ui.edit_mode_bnt.clicked.connect(self.edit_mode_change)
        self.view.ui.slider.sliderPressed.connect(self.video_thread.pause)
        self.view.ui.slider.sliderReleased.connect(self.set_frame)
        self.video_thread.changePixmap.connect(self.load_video)
        self.video_thread.changeState.connect(self.update_button)

    def init(self):
        self.load_options()
        self.view.ui.frames_label.setText("0/" + str(self.video.length_frames))
        self.view.ui.slider.setRange(0, self.home_controller.video.length_frames)
        self.video_thread.set_video(self.video)
        self.view.refined_video.init()
        self.view.original_video.init()

    def run(self):
        self.init()
        self.video_thread.start()
        self.view.show()

    @QtCore.Slot(QtGui.QPixmap, int)
    def load_video(self, image, frame_id):
        # Update number of frame
        self.update_frame_count(frame_id)
        self.slider_update(frame_id)

        # Set detection list on Original Video
        if self.home_controller.original_track_list:
            original_frame_tracked_objects = self.home_controller.original_track_list.get_all_objects(frame_id)
            original_detection = []
            for c in original_frame_tracked_objects:
                original_detection.append(c.detection_on_frame(frame_id))
            self.view.original_video.set_detection_list(original_detection)

        # Set detection list on Refined Video
        if self.home_controller.refined_track_list:
            refined_frame_tracked_objects = self.home_controller.refined_track_list.get_all_objects(frame_id)
            refined_detection = []
            for c in refined_frame_tracked_objects:
                refined_detection.append(c.detection_on_frame(frame_id))
            self.view.refined_video.set_detection_list(refined_detection)

        self.view.original_video.set_frame(image)
        self.view.refined_video.set_frame(image)

    @QtCore.Slot(bool)
    def update_button(self, playing):
        if playing:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.view.ui.play_bnt.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPlay))

    def set_frame(self):
        """Set frame number according to the slider's position"""
        self.video_thread.jump_frame_slot(self.view.ui.slider.value())

    def slider_update(self, position):
        self.view.ui.slider.setValue(position)

    def update_frame_count(self, frame_number):
        self.view.ui.frames_label.setText("Frames: " + str(frame_number) + "/" +
                                          str(self.home_controller.video.length_frames))

    def play(self):
        if self.video_thread.playing:
            self.video_thread.pause()
        else:
            self.video_thread.play()
            if self.edit_mode:  # Edit mode cannot be used while the video is being played
                self.edit_mode_change()

    def edit_mode_change(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.view.ui.edit_mode_bnt.setText("Edit Mode (ON)")
            self.view.ui.edit_mode_bnt.setStyleSheet("background-color:#83CF74;")
            self.video_thread.pause()
        else:
            self.view.ui.edit_mode_bnt.setText("Edit Mode (OFF)")
            self.view.ui.edit_mode_bnt.setStyleSheet("background-color:#BABABA;")

        for recognition in self.view.refined_video.scene_recognition:
            recognition.set_edit_mode(self.edit_mode)

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
    changePixmap = QtCore.Signal(QtGui.QPixmap, int)
    changeState = QtCore.Signal(bool)

    def __init__(self, video=None):
        super(VideoThread, self).__init__()
        self.video = video
        self.playing = False
        self.current_frame = 0

    def set_video(self, video):
        self.video = video

    def next_frame_slot(self):
        # xfce4-taskmanager
        ret, frame = self.video.cv.read()
        if ret:
            image_cv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = QtGui.QImage(image_cv.data, image_cv.shape[1], image_cv.shape[0],
                                  QtGui.QImage.Format_RGB888)

            # Fixing memory leak bug at Pyside QImage constructor
            ctypes.c_long.from_address(id(image_cv)).value = 1

            self.current_frame = self.video.cv.get(cv2.CAP_PROP_POS_FRAMES)
            self.changePixmap.emit(QtGui.QPixmap.fromImage(frame), self.current_frame)

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