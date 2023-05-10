import sys

from loguru import logger
from PyQt6 import QtWidgets, QtCore

from .window import AbstractWindow, AbstractMessage
from .widgets import TextButton

"""
Application entry point / Точка входа приложения.

"""


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = AbstractWindow()
        self.window.setStyleSheet("background-color: white;")
        self.window.setMinimumSize(720, 480)
        self.window.show()
        message1 = AbstractMessage(self.window, QtCore.QRect(20, 20, 200, 200))
        message2 = AbstractMessage(self.window, QtCore.QRect(50, 50, 200, 200), message1)
        message1.show()
        message2.show()
        button = TextButton("circle", "hello")
        l = QtWidgets.QGridLayout(message2.island)
        l.addWidget(button)
        logger.debug("all ready to start")
        sys.exit(self.exec())
