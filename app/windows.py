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
        absw.AbstractWindow.__init__(self, parent)
        self.signals.close.connect(self.on_close)
        self.setObjectName(name)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        logger.debug(f"{self.objectName()} window showed")
        return super().showEvent(a0)

    def on_close(self):
        d = dialogs.YesNoDialog(self, "Закрыть приложение?")
        d.setFixedHeight(200)
        d.accepted.connect(self.close)
        d.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(f"{self.objectName()} window closed")
        return super().closeEvent(a0)