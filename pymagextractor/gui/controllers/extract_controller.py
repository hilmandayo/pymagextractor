from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.gui.views.extract_view import ExtractView
from PySide2.QtWidgets import QStyle
import cv2, time
from pymagextractor.models.buffer.frame import Frame


class ExtractController(QtCore.QObject):

    def __init__(self, home_controller):
        super(ExtractController, self).__init__()
        self.home_controller = home_controller
        self.video_thread = VideoThread(self)
        self.view = ExtractView(self)
        # TODO: Commenting out below approach for a moment.
        # self.video = self.home_controller.video
        self.original_tl = None
        self.refined_tl = None

        # Modes
        self.edit_mode = False

        # Connect all signals
        self.view.ui.play_bnt.clicked.connect(self.play)
        self.view.ui.edit_mode_bnt.clicked.connect(self.edit_mode_change)
        self.view.ui.previous_bnt.clicked.connect(self.previous_obj)
        self.view.ui.next_bnt.clicked.connect(self.next_obj)
        self.view.ui.slider.sliderPressed.connect(self.video_thread.pause)
        self.view.ui.slider.sliderReleased.connect(self.jump_to_frame)
        self.video_thread.changeFrame.connect(self.load_video)
        self.video_thread.changeState.connect(self.update_button)

    def init(self):
        self.video = self.home_controller.video
        self.original_tl = self.home_controller.original_track_list
        self.refined_tl = self.home_controller.refined_track_list

        self.view.ui.previous_bnt.setEnabled(self.refined_tl is not None)
        self.view.ui.next_bnt.setEnabled(self.refined_tl is not None)

        self.load_options()
        self.view.ui.slider.setRange(0, self.video.n_frames-1)
        self.update_labels()

        self.video_thread.set_video(self.video)
        self.video_thread.set_frames_sequence(self.video.frames_sequence)

        self.view.refined_video.init()
        self.view.original_video.init()

    def run(self):
        self.init()
        self.video_thread.start()
        self.view.show()

    @QtCore.Slot(Frame, int)
    def load_video(self, frame, frame_sequence_index):
        video_frame_id = frame.frame_id
        image = frame.image

        self.update_labels(frame_sequence_index + 1)
        self.slider_update(frame_sequence_index)

        # Set detection list on Original Video
        if self.original_tl:
            original_frame_tracked_objects = self.original_tl.get_all_objects(video_frame_id)
            original_detection = []
            for c in original_frame_tracked_objects:
                original_detection.append(c.detection_on_frame(video_frame_id))
            self.view.original_video.set_detection_list(original_detection)

        # Set detection list on Refined Video
        if self.refined_tl:
            refined_detection = []
            if not self.refined_tl.is_object_selected():  # Get all objects in the frame
                refined_frame_tracked_objects = self.refined_tl.get_all_objects(video_frame_id)
                for c in refined_frame_tracked_objects:
                    refined_detection.append(c.detection_on_frame(video_frame_id))
            else:  # Get only selected object
                refined_detection.append(self.refined_tl.get_current_object().detection_on_frame(video_frame_id))
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

    def jump_to_frame(self):
        """Set frame number according to the slider's position"""
        self.video_thread.jump_frame(self.view.ui.slider.value())

    def slider_update(self, position):
        self.view.ui.slider.setValue(position)

    def update_labels(self, tracked_frame_id=0):
        self.view.ui.frames_label.setText("Video Frames: " + str(int(self.video.current_frame_id)) + "/" + str(self.video.n_frames))
        if self.refined_tl:
            self.view.ui.objects_label.setText("Objects: " + str(self.refined_tl.index + 1) +
                                               "/" + str(len(self.refined_tl.tracked_objects)))
            if self.refined_tl.is_object_selected():
                self.view.ui.object_frames_label.setText("Tracked Frames: " + str(tracked_frame_id) + "/"
                                                         + str(self.refined_tl.get_current_object().number_of_frames()))

    def play(self):
        if self.video_thread.playing:
            self.video_thread.pause()
        else:
            self.video_thread.play()
            if self.edit_mode:  # Edit mode cannot be used while the video is being played
                self.edit_mode_change()

    def previous_obj(self):
        new_object = self.refined_tl.get_previous_object()
        if new_object:
            frames_sequence = new_object.frames_sequence()
        else:  # When object number is zero show complete video
            frames_sequence = self.video.frames_sequence

        self.video_thread.set_frames_sequence(frames_sequence)
        self.video_thread.next_frame()
        self.view.ui.slider.setRange(0, len(frames_sequence)-1)
        self.update_labels(1)

    def next_obj(self):
        new_object = self.refined_tl.get_next_object()
        if new_object:
            frames_sequence = new_object.frames_sequence()
        else:  # When object number is zero show complete video
            frames_sequence = self.video.frames_sequence

        self.video_thread.set_frames_sequence(frames_sequence)
        self.video_thread.next_frame()
        self.view.ui.slider.setRange(0, len(frames_sequence)-1)
        self.update_labels(1)

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
    changeFrame = QtCore.Signal(Frame, int)
    changeState = QtCore.Signal(bool)

    def __init__(self, controller, video=None):
        super(VideoThread, self).__init__()
        self.controller = controller
        self.video = video
        self.playing = False

        self.frames_sequence_ids = []
        self.frame_sequence_index = 0
        self.last_frame_id = 0

    def set_video(self, video):
        """Set video"""
        self.video = video

    def set_frames_sequence(self, frames_sequence_ids):
        self.frames_sequence_ids = frames_sequence_ids
        self.frame_sequence_index = -1

    def play(self):
        self.playing = True
        self.changeState.emit(self.playing)

    def pause(self):
        self.playing = False
        self.changeState.emit(self.playing)

    def next_frame(self):
        # If it's not the last frame
        if self.frame_sequence_index < (len(self.frames_sequence_ids) - 1):

            self.frame_sequence_index += 1
            current_frame_id = self.frames_sequence_ids[self.frame_sequence_index]

            if current_frame_id == self.last_frame_id + 1:
                self.changeFrame.emit(self.video.next_frame_slot(), self.frame_sequence_index)
            else:
                self.changeFrame.emit(self.video.jump_frame_slot(current_frame_id), self.frame_sequence_index)

            self.last_frame_id = current_frame_id

        else:
            self.pause()

    def previous_frame(self):
        # if it's not the first frame
        if self.frame_sequence_index > 0:
            self.frame_sequence_index -= 1
            current_frame_id = self.frames_sequence_ids[self.frame_sequence_index]
            self.changeFrame.emit(self.video.jump_frame_slot(current_frame_id), self.frame_sequence_index)
            self.last_frame_id = current_frame_id

    def jump_frame(self, frame_index):
        if 0 <= frame_index < len(self.frames_sequence_ids):
            self.frame_sequence_index = frame_index
            current_frame_id = self.frames_sequence_ids[self.frame_sequence_index]
            self.changeFrame.emit(self.video.jump_frame_slot(current_frame_id), self.frame_sequence_index)
            self.last_frame_id = current_frame_id

    def run(self):
        while True:
            while self.playing:
                self.next_frame()
                time.sleep(1/self.video.fps)
            time.sleep(0.1)
