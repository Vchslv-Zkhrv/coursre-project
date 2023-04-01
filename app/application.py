import sys
from pprint import pprint
import inspect

from loguru import logger
from PyQt6 import QtWidgets
import pyqt_custom_titlebar_window as ctw

from .qwindows import Window

"""
Application entry point / Точка входа приложения.

"""


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = Window()
        ctw.customTitlebarWindow.FramelessWindow()
        self.window.show()
        logger.debug("all ready to start")
        sys.exit(self.exec())
