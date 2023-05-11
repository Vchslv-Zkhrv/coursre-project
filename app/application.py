import sys
from typing import Literal

from PyQt6 import QtWidgets

from .windows import MainWindow
from . import qt_shortcuts as shorts
from . import widgets
from . import events
from . import custom_widgets as custom
from . import config as cfg
from . import dialogs
from .config import rgba, CURRENT_THEME as THEME

"""
Application entry point / Точка входа приложения.

"""


class Window(MainWindow):

    """
    Main application window /
    Главное окно приложения
    """

    mode: Literal["auth", "main"]

    def __init__(self):
        MainWindow.__init__(self, "main")
        self.auth_signals = events.AuthorizationSignals()
        self.setMinimumSize(720, 480)
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['back'])};
            border: none;""")
        self.mode = "auth"
        self.signals.info.connect(self.show_help)

    def show_help(self):
        if self.mode == "auth":
            dialog = dialogs.AlertDialog(
                "info-auth",
                self,
                "Введите данные вашей учетной записи, чтобы продолжить")
            dialog.title.setText("Подсказка")
            dialog.show()


class Application(QtWidgets.QApplication):

    """main application class / главный класс приложения"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.window = Window()
        self.window.show()
        sys.exit(self.exec())
