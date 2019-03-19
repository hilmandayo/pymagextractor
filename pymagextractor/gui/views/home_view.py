from PySide2 import QtCore, QtWidgets
from pymagextractor.gui.qt_windows.home import Ui_HomeWindow


class HomeView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(HomeView, self).__init__()
        self.controller = controller
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_A:
            self.controller.add_object()
        else:
            super().keyPressEvent(qKeyEvent)