import PySide2
from PySide2.QtWidgets import QDesktopWidget
import typing

class Screen(object):
  def __init__(self):
    self.primary_screen: int = 1

  def get_screen_geometry(self):
    return QDesktopWidget.screenGeometry()

