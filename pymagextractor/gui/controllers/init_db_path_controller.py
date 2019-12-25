import sys
from pathlib import Path
import toml

import PySide2
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QLineEdit,
                               QGraphicsColorizeEffect, QGroupBox, QLabel, QMainWindow,
                               QPlainTextEdit, QPushButton, QStackedWidget, QTabWidget, QTextEdit, QInputDialog,)
from PySide2.QtGui import QIcon, QColor, QScreen
from PySide2.QtCore import Qt, QEvent, QPoint, QSize, QSettings

from pymagextractor.gui.views.init_db_view import DbInitView
from pymagextractor.gui.controllers.home_controller import HomeController
from pymagextractor.models.database import DataBase
from pathlib import Path


class InitDatabasePathController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.path_to_db = None
        self.view = DbInitView(self)
        self.pymagextractor_config_dir = Path.home() / ".config" / "pymagextractor"
        if not self.pymagextractor_config_dir.exists():
            self.pymagextractor_config_dir.mkdir(parents=True)

        self.db_path_file = self.pymagextractor_config_dir / "db_path"
        # self.db_path_list ={'database_paths' : {'list':[],
        #                                         'last_opened': None}}

        self.init()

    def init(self):
        self.view.ui.db_btn_search.clicked.connect(self.search_path)
        self.view.ui.db_btn_generate.clicked.connect(self.create_db_file)

    def search_path(self):

        self.path_to_db = QFileDialog.getExistingDirectory()
        self.view.ui.db_box_path.setText(self.path_to_db)
        self.view.ui.db_box_path.textChanged.connect(self.view.ui.db_btn_generate.setEnabled(True))

    def create_db_file(self):
        self.db_path_file.write_text(f"{self.path_to_db}\n")
        PySide2.QtCore.QCoreApplication.instance().quit()
        # self.db_path_list['database_paths']['list'].append(self.path_to_db)
        # self.db_path_list['database_paths']['last_opened'] = self.path_to_db
        # self.create_db_folders()
        # toml.dump(self.db_path_list, open(self.db_filename, mode='w'))


    # def create_db_folders(self):
    #     print("hwhwhwhwhwhwhwhwhwhw")
    #     self.db_folders = DataBase(self.path_to_db)

    def run(self):
        self.view.show()
        return self.app.exec_()
