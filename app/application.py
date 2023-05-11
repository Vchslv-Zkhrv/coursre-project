import sys

from loguru import logger
from PyQt6 import QtWidgets

from .window import AbstractWindow
from . import dialogs
from . import widgets

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
        dialog = dialogs.Dialog(self.window, "alarm-clock", "Hello World")
        dialog.setFixedSize(600, 400)
        l = QtWidgets.QVBoxLayout(dialog.body)
        dialog.body.layout().addWidget(widgets.TextButton("brain-circuit", "hello"))
        dialog.show()
        dialog.exec()
        logger.debug("all ready to start")
        sys.exit(self.exec())
