import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.home import Ui_HomeWindow


class HomeView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(HomeView, self).__init__()
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)

