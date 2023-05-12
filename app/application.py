import sys
from typing import Literal

from PyQt6 import QtWidgets
from loguru import logger

from .windows import MainWindow
from . import qt_shortcuts as shorts
from . import events
from . import dialogs
from . import connector
from . import forms
from . import groups
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
        shorts.GLayout(self.content)
        self.auth_form = forms.AuthForm()
        # self._draw_auth_form()
        self._draw_main_form()

    def _draw_auth_form(self):
        self.content.layout().addWidget(self.auth_form)
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
            logger.debug("AUTHORIZATION FAILED")
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
        logger.debug("AUTHORIZATION SUCCESS")
        self.mode = "main"
        self._draw_main_form()

    def _draw_main_form(self):
        self.auth_form.hide()
        self.signals.info.disconnect()
        self.toolbar = groups.ToolBar(self)
        self.title_bar.layout().addWidget(self.toolbar)

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

    def run(self) -> int:
        self.window = Window()
        self.window.show()
        exit_code = self.exec()
        logger.debug("FINSH")
        return exit_code
