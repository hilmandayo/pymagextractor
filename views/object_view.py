from PySide2 import QtCore, QtGui, QtWidgets
from frontend.object_info import Ui_Form


class ObjectView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ObjectView, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
