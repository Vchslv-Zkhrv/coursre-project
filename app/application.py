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
    users_database: connector.SqlUsers
    database: connector.Connection
    log_in_attempts: int = 3

    def __init__(self):
        MainWindow.__init__(self, "main")
        self.auth_signals = events.AuthorizationSignals()
        self.setMinimumSize(720, 480)
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['back'])};
            border: none;""")
        self.mode = "auth"
        self.signals.info.connect(self.show_help)
        self.users_database = connector.SqlUsers()
        self.draw_auth_form()

    def draw_auth_form(self):
        self.auth_form = forms.AuthForm()
        clayout = shorts.GLayout(self.content)
        clayout.addItem(shorts.VSpacer(), 0, 1, 1, 1)
        clayout.addItem(shorts.VSpacer(), 1, 0, 1, 1)
        clayout.addWidget(self.auth_form, 1, 1, 1, 1)
        clayout.addItem(shorts.VSpacer(), 1, 2, 1, 1)
        clayout.addItem(shorts.VSpacer(), 2, 1, 1, 1)
        self.auth_form.signals.send.connect(self._on_log_in_clicked)

    def _show_log_in_error(self):
        if self.log_in_attempts in (2, 3):
            message = f"Осталось {self.log_in_attempts} попытки"
        elif self.log_in_attempts == 1:
            message = "Осталась последняя попытка"
        else:
            message = "Превышено максимальное число попыток. Приложение будет закрыто"
        dialog = dialogs.AlertDialog(
            "wrong log in alert",
            self,
            f"Данные неверны.\n\n{message}")
        if self.log_in_attempts == 0:
            dialog.rejected.connect(lambda: self.close())
        dialog.show()
        self.log_in_attempts -= 1

    def _on_log_in_clicked(self):
        data = self.auth_form.collect()
        try:
            correct = self.users_database.log_in(data["login"], data["password"])
        except AttributeError:
            return
        if not correct:
            self._show_log_in_error()
            return

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
