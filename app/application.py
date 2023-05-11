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
from . import connector
from . import forms
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
    database: connector.Connection

    def __init__(self):
        MainWindow.__init__(self, "main")
        self.auth_signals = events.AuthorizationSignals()
        self.setMinimumSize(720, 480)
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['back'])};
            border: none;""")
        self.mode = "auth"
        self.signals.info.connect(self.show_help)
        self.database = connector.SqlUsers()
        self.draw_auth_form()

    def draw_auth_form(self):
        self.auth_form = forms.AuthForm()
        clayout = shorts.GLayout(self.content)
        clayout.addItem(shorts.VSpacer(), 0, 1, 1, 1)
        clayout.addItem(shorts.VSpacer(), 1, 0, 1, 1)
        clayout.addWidget(self.auth_form, 1, 1, 1, 1)
        clayout.addItem(shorts.VSpacer(), 1, 2, 1, 1)
        clayout.addItem(shorts.VSpacer(), 2, 1, 1, 1)

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
