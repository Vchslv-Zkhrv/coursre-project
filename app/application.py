import sys

from loguru import logger
from PyQt6 import QtWidgets

from .qwindows import Window
from . import qt_shortcuts
from . import custom_widgets

"""
Application entry point / Точка входа приложения.

"""


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = Window()
        b = custom_widgets.SvgLabel("alarm-clock")
        self.window.layout().addWidget(b)
        self.window.show()
        logger.debug("all ready to start")
        sys.exit(self.exec())
