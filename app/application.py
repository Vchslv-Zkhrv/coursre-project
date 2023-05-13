from typing import Literal

from PyQt6 import QtWidgets
from loguru import logger

from .window import Window
from . import connector


"""
Application entry point /
Точка входа приложения.
"""


class Application(QtWidgets.QApplication):

    """
    main application class /
    главный класс приложения
    """

    mode: Literal["auth", "nofile", "main"]
    application_database: connector.SqlUsers
    working_database: connector.Connection
    log_in_attempts: int = 3

    def __init__(self, argv: tuple[str]) -> None:
        super().__init__(argv)
        self.window = Window()
        self.window.signals.info.connect(self.show_help)
        self.application_database = connector.SqlUsers()

    def run(self) -> int:
        self.window.show()
        self.authentification()
        exit_code = self.exec()
        logger.debug("FINSH")
        return exit_code

    def switch_mode(self, mode: Literal["main", "auth", "nofile"]):
        self.mode = mode
        self.window.show_form(mode)

    def authentification(self):
        self.switch_mode("auth")
        self.window.forms["auth"].signals.send.connect(
            lambda result: self.log_in(result["login"], result["password"]))

    def log_in(self, login: str, password: str):
        if not login or not password:
            return
        if self.application_database.log_in(login, password):
            self.log_in_success()
        else:
            self.log_in_failed()
            self.log_in_attempts -= 1

    def log_in_success(self):
        logger.debug("AUTHORIZATION SUCCESS")
        self.window.auth_signals.correct.emit()

    def log_in_failed(self):
        if self.log_in_attempts > 0:
            logger.debug("AUTHORIZATION ATTEMPT FAILED")
            self.window.auth_signals.incorrect.emit(self.log_in_attempts)
        else:
            logger.debug("AUTHORIZATION BLOCK")
            self.window.auth_signals.suspicious.emit()

    def show_help(self):
        self.window.show_help(self.mode)
