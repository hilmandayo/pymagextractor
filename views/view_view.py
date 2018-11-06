from PySide2 import QtCore, QtGui, QtWidgets
from frontend.new_view import Ui_Form


class ViewView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ViewView, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
