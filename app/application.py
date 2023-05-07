import sys

from loguru import logger
from PyQt6 import QtWidgets

from .window import Window

"""
Application entry point / Точка входа приложения.

"""


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = Window()
        self.window.setStyleSheet("background-color: white;")
        self.window.setMinimumSize(720, 480)
        self.window.show()
        logger.debug("all ready to start")
        sys.exit(self.exec())
