''''
Most of what we the widgets or GUI related to home(extract) can be edited in this file
'''

import sys
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QLineEdit,
                               QGraphicsColorizeEffect, QGroupBox, QLabel, QMainWindow,
                               QPlainTextEdit, QPushButton, QStackedWidget, QTabWidget, QTextEdit, QInputDialog)
from PySide2.QtGui import QIcon, QColor
from PySide2.QtCore import Qt, QEvent, QPoint, QSize, QSettings
from pymagextractor.gui.views.home_view import HomeView
from pymagextractor.gui.controllers.extract_controller import ExtractController
from pymagextractor.gui.controllers.object_controller import ObjectController
from pymagextractor.models.buffer.video import Video
from pymagextractor.models.config.optionsDB import OptionsDB
from pymagextractor.models.container.track_list import TrackList
from pymagextractor.models.csv_handler import CSVHandler
from pymagextractor.models.database import DataBase
import toml


class HomeController:

    def __init__(self):
        self.app = QApplication(sys.argv)
        # List of models


        # TODO: Try different approach.
        # self.video = Video()
        self.video = None
        self.optionsDB = OptionsDB()

        self.csv_original_path = None
        self.csv_refined_path = None


        self.load_workspace_list = toml.load(open('.workspace_list.toml'))
        self.database = None
        self.database_path = None
        self.annotation_file_path = None
        self.workspace_folder = None
        self.workspace_new_name = None
        self.workspace_list = self.load_workspace_list['workspace']['name']
        self.selected_workspace = None

        self.original_track_list = None
        self.refined_track_list = None

        # View
        self.view = HomeView(self)

        # List of controllers
        self.extractor_controller = ExtractController(self)
        self.object_controller = ObjectController(self)
        
        self.init()
        self.update_ws_list()
        self.update()

    def init(self):
        """Initial setup for connecting all events"""
        self.view.ui.search_bnt.clicked.connect(self.search_video)
        self.view.ui.search_original_bnt.clicked.connect(self.search_csv_original)
        self.view.ui.search_refined_bnt.clicked.connect(self.search_csv_refined)
        self.view.ui.start_bnt.clicked.connect(self.start)
        self.view.ui.add_bnt.clicked.connect(self.add_object)
        self.view.ui.object_list.clicked.connect(self.on_listview)
        self.view.ui.save_bnt.clicked.connect(self.save_options)
        self.view.ui.load_bnt.clicked.connect(self.load_options)
        
        """Workspace-tab buttons connection"""
        self.view.ui.ws_new_search_btn.clicked.connect(self.get_new_workspace_path)
        self.view.ui.ws_new_create_btn.clicked.connect(self.create_new_workspace)
        self.view.ui.ws_new_name.text()

    def update(self):
        """Update for every time the controller is called"""
        self.update_object_list()
        self.update_files_browser()

    def run(self):
        """Open home window"""
        self.view.show()
        return self.app.exec_()

    def search_video(self):
        """Find video path"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.view, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            # self.video.set_path(file_path)

            # TODO: Try different approach.
            self.video = Video(file_path)

        self.update()
    
    
    def get_new_workspace_path(self):
        """Find new workspace directory path"""
        if self.load_workspace_list['database_dir']['path'] == "empty":
            folder_path = QFileDialog.getExistingDirectory()
            self.database_path = folder_path
            self.database = DataBase(self.database_path)
            self.load_workspace_list['database_dir']['path'] = str(self.database_path)
            toml.dump(self.load_workspace_list, open('.workspace_list.toml', mode='w'))
            self.update_workspace_path()
        else:
            self.database_path = self.load_workspace_list['database_dir']['path']
            self.database = DataBase(self.database_path)
            self.update_workspace_path()

    def update_workspace_path(self):
        self.view.ui.ws_database_path.setText(self.database_path)
        self.view.ui.ws_new_create_btn.setEnabled(True)
    

    def create_new_workspace(self):
        '''
        create the folder, copy the annotation list, and write the path into ".workspace_list.toml"
        '''
        self.workspace_new_name = self.view.ui.ws_new_name.text()
        self.selected_workspace = self.database.new_workspace(self.workspace_new_name)
        self.load_workspace_list['workspace']['name'].append(str(self.workspace_new_name))
        toml.dump(self.load_workspace_list, open('.workspace_list.toml', mode='w'))
        self.update_ws_list()
        print(self.workspace_list)

    def update_ws_list(self):
        self.view.ui.ws_select_ws_list.clear()
        for i, ws_name in enumerate(self.workspace_list):
            self.view.ui.ws_select_ws_list.addItem(str(ws_name))        
    
    #End workspace config

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

    def start(self):
        """Open video display window"""
        self.extractor_controller.run()

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
            self.view.ui.video_browser.setText(self.video.path)
        if self.csv_original_path:
            self.view.ui.csv_original_browser.setText(self.csv_original_path)
        if self.csv_refined_path:
            self.view.ui.csv_refined_browser.setText(self.csv_refined_path)

        if (self.video and self.video.path) and (self.csv_original_path or self.csv_refined_path):
            self.view.ui.start_bnt.setEnabled(True)

    def on_listview(self, index):
        self.object_controller.run(self.optionsDB.object_list[index.row()])
