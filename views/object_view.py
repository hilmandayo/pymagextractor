from PySide2 import QtCore, QtGui, QtWidgets
from frontend.object_info import Ui_Form


class ObjectView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super(ObjectView, self).__init__()
        self.controller = controller
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.controller.save()
        else:
            super().keyPressEvent(qKeyEvent)
