''''
Most of what we the widgets or GUI related to home(extract) can be edited in this file
'''

import sys
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QLineEdit,
                               QGraphicsColorizeEffect, QGroupBox, QLabel, QMainWindow,
                               QPlainTextEdit, QPushButton, QStackedWidget, QTabWidget, QTextEdit, QInputDialog)
from PySide2.QtGui import QIcon, QColor, QScreen
from PySide2.QtCore import Qt, QEvent, QPoint, QSize, QSettings
from pymagextractor.gui.views.home_view import HomeView
from pymagextractor.gui.controllers.extract_controller import ExtractController
from pymagextractor.gui.controllers.object_controller import ObjectController
from pymagextractor.gui.controllers.image_extract_controller import ImageExtractController
from pymagextractor.models.buffer.video import Video
from pymagextractor.models.config.optionsDB import OptionsDB
from pymagextractor.models.container.track_list import TrackList
from pymagextractor.models.csv_handler import CSVHandler
from pymagextractor.models.database import DataBase
from pymagextractor.toml._toml import TomlHandler
from pathlib import Path
import toml

from pymagextractor.models.database import DataID


class HomeController:

    def __init__(self, db_path_file: Path):
        self.app = QApplication(sys.argv)
        # List of models
        self.debug = True

        # TODO: Try different approach.
        # self.video = Video()
        self.video = None
        self.optionsDB = OptionsDB()

        self.csv_original_path = None
        self.csv_refined_path = None

        self.db_path_file = db_path_file
        self.new_database_path = None
        # self.db_path_list = toml.load(open(self.db_path_file))
        self.db_path_list = self.db_path_file.read_text().strip()
        self.screen = {'width':0, 'height':0}
        #Workspaces-tab
        self.database = None
        self.database_path = None
        self.database_info = None
        self.workspace_folder = None
        self.workspace_new_name = None
        self.workspace_list = None
        self.selected_workspace = None


        #Annotations-tab
        self.anns = None
        self.annotation_file_path = None
        self.scene = []
        self.object = []
        self.view = {'object':[], 'view':[], 'shortcut':[]}

        # View
        self.view = HomeView(self)

        # List of controllers
        # self.extractor_controller = ExtractController(self)
        self.image_extract_controller = ImageExtractController(self)
        self.object_controller = ObjectController(self)
        try:
            self.get_database_info()
        except:
            pass

        self.init()

        self.update()

    def init(self):
        """Initial setup for connecting all events"""
        self.view.ui.extract_search_video_bnt.clicked.connect(self.search_video)
        self.view.ui.extract_search_original_bnt.clicked.connect(self.search_csv_original)
        self.view.ui.extract_search_refined_bnt.clicked.connect(self.search_csv_refined)
        self.view.ui.extract_start_bnt.clicked.connect(self.start)
        self.view.ui.extract_img_extractor_btn.clicked.connect(self.start_image_extractor)
        self.view.ui.extract_launch_single_mode_btn.clicked.connect(self.start)
        self.view.ui.extract_launch_dual_mode_btn.clicked.connect(self.start)

        """Db paths"""
        # self.view.ui.ws_database_path.setText(self.db_path_list['database_paths']['last_opened'])
        self.view.ui.ws_database_path.setText(self.db_path_list)
        self.database_path = self.view.ui.ws_database_path.text()
        self.database = DataBase(self.database_path)
        self.database.get_db_information()
        self.enable_create_ws_button()
        self.view.ui.ws_new_name.textChanged.connect(self.new_ws_name_is_available)
        self.view.ui.ws_database_path.textChanged.connect(self.db_path_is_available)


        """Workspace-tab buttons connection"""
        # self.view.ui.ws_new_search_btn.clicked.connect(self.get_new_workspace_path)
        self.view.ui.ws_btn_new_create.clicked.connect(self.create_new_workspace)
        self.view.ui.ws_new_name.text()
        self.view.ui.ws_select_ws_list.itemSelectionChanged.connect(self.select_workspace_from_list)
        self.view.ui.ws_btn_select_ws.clicked.connect(self.confirm_workspace_selection)
        print(self.app.desktop().availableGeometry())
        """Annotations-tab buttons connection"""
        try:
            self.workspace_list = self.database.db_info['workspaces']
            self.update_ws_list()
        except:
            pass

    def get_available_database(self):
        '''
        If the user is opening for the first time, a return None.

        If the user is opening the program for the second time, load the opened
        database path in the font combo box
        '''
        try:
            self.db_path_list = toml.load(open(self.db_path_file))

        except FileNotFoundError:
            pass

        if self.debug:
            try:
                print(self.db_path_list['database_paths']) #kurogane1031 kurogane1031 kurogane1031
            except KeyError:
                print('your db file is corrupted. Delete it')

    def update_db_path_list(self):
        '''
        If there is any new database path specified by the user, the database path
        is updated.
        '''
        self.db_path_list['database_paths']['list'].append(self.new_database_path)
        self.db_path_list['database_paths']['last_opened'] = self.new_database_path
        toml.dump(self.db_path_list, open(self.db_path_file, mode='w'))

    def get_new_workspace_path(self):
        """Find new workspace directory path"""
        self.workspace_list = self.database.db_info['workspaces']
        print(self.workspace_list)
        self.update_workspace_path()
        self.update_ws_list()

    def new_ws_name_is_available(self):
        '''
        check if ```name of workspace``` is available or not.
        '''
        self.workspace_new_name = self.view.ui.ws_new_name.text()
        self.enable_create_ws_button()

    def db_path_is_available(self):
        '''
        check if the database path is specified or not.
        '''
        self.new_database_path = self.view.ui.ws_database_path.setText(self.database_path)
        print(self.new_database_path)
        self.enable_create_ws_button()

    def update_workspace_path(self):
        self.view.ui.ws_database_path.setText(self.database_path)

    def enable_create_ws_button(self):
        if (self.workspace_new_name):
            self.view.ui.ws_btn_new_create.setEnabled(True)

    def create_new_workspace(self):
        '''
        create the folder, copy the annotation list, and write the path into ".workspace_list.toml"
        '''
        self.new_database_path = self.view.ui.ws_database_path.text()
        # self.update_db_path_list()
        self.selected_workspace = self.database.new_workspace(self.workspace_new_name)
        self.update_ws_list()

    def update_ws_list(self):
        '''
        Refreshes available workspace list
        '''
        self.view.ui.ws_select_ws_list.clear()
        for i, ws_name in enumerate(self.workspace_list):
            self.view.ui.ws_select_ws_list.addItem(str(ws_name))

    def select_workspace_from_list(self):
        '''
        ```Select Workspace``` button only will work if one of the item in the list is selected.
        '''
        self.view.ui.ws_btn_select_ws.setEnabled(True)

    def confirm_workspace_selection(self):
        '''
        Confirm selection of previous available workspace.
        New annotation instances will be created each time ```Select Workspace``` button is selected.
        '''
        self.selected_workspace = self.view.ui.ws_select_ws_list.currentItem().text()
        print(self.selected_workspace)
        print(self.database_path)
        self.image_extract_controller.ws = self.selected_workspace
        self.image_extract_controller.ws_path = self.database_path
        self.annotation_file_path = self.database_path + "/settings/workspaces_annotations/" + self.selected_workspace + ".toml"
        self.anns = TomlHandler()
        self.update_annotation_ws()
    #End workspace config


    def update(self):
        """Update for every time the controller is called"""
        # self.update_object_list()
        self.update_files_browser()

    def run(self):
        """Open home window"""
        self.view.show()
        return self.app.exec_()

    def search_video(self):
        """Find video path"""
        # XXX: For this time being, it would be the gateway to data id
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # file_path, _ = QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
        #                                                     "All Files (*);;Python Files (*.py)", options=options)

        # XXX: This is just on reading...
        data_id_path = QFileDialog.getExistingDirectory(
            self.view, "Select Data ID", self.database[self.selected_workspace].workspace_path, options=options)

        # if file_path:
        #     # self.video.set_path(file_path)

        #     # TODO: Try different approach.
        #     self.video = Video(file_path, width=640, height=500)

        print(data_id_path)
        if Path(data_id_path).exists():
            data_id = DataID(data_id_path)
            p = data_id.buffer
            self.video = Video(str(p), width=640, height=500)

        # p = Path(file_path)
        self.video_name = p.stem
        self.image_extract_controller.view.image_viewer.video_filename_ = self.video_name
        self.update()


    #Start annotations config
    def update_annotations_list(self):
        '''
        List out all available notations.
        If notation not exist, a default one will be written first.
        '''
        self.view.ui.ann_lists.clear()
        arrow = u"\u2192"
        for i, name in enumerate(self.anns.anns['annotations']):
            self.scene.append(name)
            self.image_extract_controller.add_scene_list = self.scene
            for j, ann_object in enumerate(name['object_id']):
                self.view.ui.ann_lists.addItem(str([name['scene'], ann_object]))
                for k, ann_view in enumerate(name[ann_object]):
                    self.view.ui.ann_lists.addItem(str([arrow, ann_view]))

    def update_annotation_ws(self):
        '''
        Update some information in the Annotation-tab
        '''
        self.anns._workspace = self.view.ui.ann_cur_ws.setText(self.selected_workspace)
        # self.image_extract_controller.view.image_viewer.ws_ = self.anns._workspace
        self.anns._filename = self.annotation_file_path
        print(self.anns._filename)
        self.anns.check_if_exist()
        self.update_annotations_list()

    def add_view_to_object(self):
        print('Here here')

    #End annotations config
    def search_csv_original(self):
        """Find csv original path"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                            "CSV Files (*.csv)", options=options)
        if file_path:
            self.csv_original_path = file_path
            self.original_track_list = CSVHandler(file_path)

        self.update()

    def search_csv_refined(self):
        """Find csv refined path"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "CSV Files (*.csv)", options=options)
        if file_path:
            self.csv_refined_path = file_path
            self.refined_track_list = CSVHandler(file_path)

        self.update()

    def start_image_extractor(self):
        """Open video display window"""
        self.image_extract_controller.run()

    def start(self):
        """Open video display window"""
        # self.extractor_controller.run()

    def add_object(self):
        """Open add object window"""
        self.object_controller.run()

    def save_options(self):
        """Save objects on a xml file"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.view, "QFileDialog.getSaveFileName()", "",
                                                            "XML files (*.xml)", options=options)
        if file_name:
            if not (".xml" in file_name):
                file_name += ".xml"
            self.optionsDB.save_db(file_name)

    def load_options(self):
        """Load a xml file to a list of objects"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                             "XML files (*.xml)", options=options)
        if file_path:
            self.optionsDB.load_db(file_path)
            print(file_path)

        self.update()

    def update_object_list(self):
        self.view.ui.object_list.clear()
        for object in self.optionsDB.object_list:
            self.view.ui.object_list.addItem(object.name)

    def update_files_browser(self):
        # TODO: Try different approach.
        if self.video and self.video.path:
            self.view.ui.extract_video_browser.setText(self.video.path)
        if self.csv_original_path:
            self.view.ui.extract_csv_original_browser.setText(self.csv_original_path)
        if self.csv_refined_path:
            self.view.ui.extract_csv_refined_browser.setText(self.csv_refined_path)

        '''
        If only video is available, only ```Image Extraction``` is allowed.
        If video and only one csv is available, ```Image Extraction``` and ```Single Mode`` is allowed
        If video and two csv is available, all mode is allowed.
        '''

        if (self.video and self.video.path):
            self.view.ui.extract_img_extractor_btn.setEnabled(True)
        if (self.video and self.video.path) and (self.csv_original_path or self.csv_refined_path):
            self.view.ui.extract_launch_single_mode_btn.setEnabled(True)
        if (self.video and self.video.path) and (self.csv_original_path and self.csv_refined_path):
            self.view.ui.extract_launch_dual_mode_btn.setEnabled(True)

    def on_listview(self, index):
        self.object_controller.run(self.optionsDB.object_list[index.row()])
