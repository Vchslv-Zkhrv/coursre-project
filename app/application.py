import sys

from PyQt6 import QtWidgets

from .windows import MainWindow

"""
Application entry point / Точка входа приложения.

"""


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = MainWindow("authentification")
        self.window.setStyleSheet("background-color: white;")
        self.window.setMinimumSize(720, 480)
        self.window.show()
        sys.exit(self.exec())
