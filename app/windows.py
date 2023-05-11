from PyQt6 import QtGui, QtWidgets
from loguru import logger

from . import dialogs
from . import abstract_windows as absw


class MainWindow(absw.AbstractWindow):

    """
    Main application window class /
    Главный класс окон приложения
    """

    def __init__(self, name: str, parent: QtWidgets.QWidget = None):
        absw.AbstractWindow.__init__(self, name, parent)
        self.signals.close.connect(self.on_close)

    def on_close(self):
        d = dialogs.YesNoDialog("window closer", self, "Закрыть приложение?")
        d.setFixedHeight(200)
        d.accepted.connect(self.close)
        d.show()
