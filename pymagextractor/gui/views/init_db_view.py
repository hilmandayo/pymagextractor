from PySide2 import QtCore, QtWidgets
from pymagextractor.gui.qt_windows.init import Ui_DbPathSearchWindow

class DbInitView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(DbInitView, self).__init__()
        self.controller = controller
        self.ui = Ui_DbPathSearchWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.controller.search_path()
        else:
            super().keyPressEvent(qKeyEvent)
