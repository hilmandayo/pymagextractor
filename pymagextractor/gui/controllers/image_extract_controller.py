'''
GUI when user select image extractor mode
'''
from PySide2 import QtCore, QtGui, QtWidgets
from pymagextractor.gui.views.image_extract_view import ImageExtractView
from PySide2.QtWidgets import QStyle
import cv2, time
from pymagextractor.models.buffer.frame import Frame



class ImageExtractController(QtCore.QObject):

    def __init__(self, home_controller):
        super(ImageExtractController, self).__init__()
        self.home_controller = home_controller
        self.video_thread = VideoThread(self)
        self.view = ImageExtractView(self)
        self.original_tl = None
        # Modes
        self.edit_mode = False

        # Connect all signals
        self.view.ui.play_bnt.clicked.connect(self.play)
        self.view.ui.edit_mode_bnt.clicked.connect(self.edit_mode_change)
        # self.view.ui.previous_bnt.clicked.connect(self.previous_obj)
        # self.view.ui.next_bnt.clicked.connect(self.next_obj)
        self.view.ui.slider.sliderPressed.connect(self.video_thread.pause)
        self.view.ui.slider.sliderReleased.connect(self.jump_to_frame)
        self.video_thread.changeFrame.connect(self.load_video)
        self.video_thread.changeState.connect(self.update_button)

        # Add object dock
        self.track_id_list = [1]
        self.add_view_list = []
        self.add_scene_list = []
        self.add_object_list = []
        self.selected_track_id = None
        self.selected_object = None
        self.selected_view = None
        self.view.ui.add_track_id_btn.clicked.connect(self.add_track_id)
        self.view.ui.add_track_id_list.clicked.connect(self.get_selected_track_id)
        self.view.ui.add_object_list.clicked.connect(self.get_selected_object)
        self.view.ui.add_view_list.clicked.connect(self.get_selected_view)
        self.view.ui.add_scene_list.clicked.connect(self.get_selected_scene)
        self.view.ui.add_view_btn.clicked.connect(self.add_view)
        self.ws = None
        self.ws_path = None

    def init(self):
        self.video = self.home_controller.video
        self.update_track_id_list()         #update track id list at each initialization
        self.update_scene_list(init=0)
        self.update_object_list(init=0)
        self.update_view_list(init=0)
        self.load_options()
        self.view.ui.slider.setRange(0, self.video.n_frames-1)
        self.update_labels()
        self.video_thread.set_video(self.video)
        self.video_thread.set_frames_sequence(self.video.frames_sequence)


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
            self.view.image_viewer.set_detection_list(original_detection)

        self.view.image_viewer.set_frame(image)


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
        try:
            frame_id = str(int(self.video.current_frame_id))
        except:  # TODO: Specify the exception, after backend decided the proper exception
            frame_id = "-"

        self.view.ui.frames_label.setText(
            "Video Frames: " + frame_id + "/" + str(self.video.n_frames))
        self.view.image_viewer.current_frame_number = frame_id

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

    # start add_objects_dock
    def add_track_id(self):
        self.track_id_list.append(self.view.ui.add_track_id.text())
        self.update_track_id_list()

    def add_view(self):
        size_of_view_list = len(self.add_scene_list)
        cur_scene = self.view.ui.add_scene_list.currentRow() #should return an index integer
        cur_obj = self.view.ui.add_object_list.currentItem().text() #should return the object name

        self.add_scene_list[cur_scene][cur_obj].append(self.view.ui.add_view.text())
        self.update_view_list()

    def update_track_id_list(self):
        self.view.ui.add_track_id_list.clear()
        for i, ids in enumerate(self.track_id_list):
            self.view.ui.add_track_id_list.addItem(str(ids))

        '''
        autoselect the newly added track id
        '''
        self.view.ui.add_track_id_list.setCurrentRow(i)
        self.selected_track_id = self.view.ui.add_track_id_list.currentItem().text()
        self.view.image_viewer.current_selected_track_id = self.selected_track_id

    def update_scene_list(self, init = 0):
        '''
        update the list of scenes in object dock
        '''
        self.view.image_viewer.ws_ = self.ws
        self.view.image_viewer.ws_path_ = self.ws_path
        self.view.ui.add_scene_list.clear()
        for i, sce in enumerate(self.add_scene_list):
            self.view.ui.add_scene_list.addItem(str(sce['scene']))

        '''
        autoselect the newly added scene
        '''

        if init==0:
            self.view.ui.add_scene_list.setCurrentRow(0)
        else:
            self.view.ui.add_scene_list.setCurrentRow(i)

        self.selected_scene = self.view.ui.add_scene_list.currentItem().text()
        self.view.image_viewer.current_selected_scene = self.selected_scene

    def update_object_list(self, init = 0):
        '''
        update the list of objects in object dock
        '''
        self.view.ui.add_object_list.clear()
        cur = self.view.ui.add_scene_list.currentRow()
        for i, obj in enumerate(self.add_scene_list[cur]['object_id']):
            self.view.ui.add_object_list.addItem(str(obj))

        if init==0:
            self.view.ui.add_object_list.setCurrentRow(0)
        else:
            self.view.ui.add_object_list.setCurrentRow(i)

        self.selected_object = self.view.ui.add_object_list.currentItem().text()
        self.view.image_viewer.current_selected_object = self.selected_object

    def update_view_list(self, init = 0):
        '''
        update the list of views in object dock
        '''
        self.view.ui.add_view_list.clear()

        cur_scene = self.view.ui.add_scene_list.currentRow() #should return an index integer
        cur_obj = self.view.ui.add_object_list.currentItem().text() #should return the object name

        for i, view in enumerate(self.add_scene_list[cur_scene][cur_obj]):
            self.view.ui.add_view_list.addItem(str(view[0]))

        if init == 0:
            self.view.ui.add_view_list.setCurrentRow(0)
        else:
            self.view.ui.add_view_list.setCurrentRow(i)

        self.selected_view = self.view.ui.add_view_list.currentItem().text()
        self.view.image_viewer.current_selected_view = self.selected_view

    def get_selected_track_id(self):
        self.selected_track_id = self.view.ui.add_track_id_list.currentItem().text()
        self.view.image_viewer.current_selected_track_id = self.selected_track_id

    def get_selected_scene(self):
        self.selected_scene = self.view.ui.add_scene_list.currentItem().text()
        self.view.image_viewer.current_selected_scene = self.selected_scene
        self.update_object_list()
        self.update_view_list()

    def get_selected_object(self):
        self.selected_object = self.view.ui.add_object_list.currentItem().text()
        self.view.image_viewer.current_selected_object = self.selected_object
        self.update_view_list()

    def get_selected_view(self):
        self.selected_view = self.view.ui.add_view_list.currentItem().text()
        self.view.image_viewer.current_selected_view = self.selected_view

    # end add_objects_dock

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
