from PyQt6 import QtWidgets

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
        self.signals.maximize.connect(self.on_maximize)
        self.signals.minimize.connect(self.showMinimized)

    def on_close(self):
        d = dialogs.YesNoDialog("window closer", self, "Закрыть приложение?")
        d.island.setFixedHeight(200)
        d.accepted.connect(self.close)
        d.show()

    def on_maximize(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()
