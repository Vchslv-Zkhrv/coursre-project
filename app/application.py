from PyQt6 import QtWidgets
from loguru import logger

from .window import Window, _Window
from . import connector
from .config import FORMS
from . import actions
from . import dialogs
from . import config as cfg
from .personalization import theme_switcher

"""
Application entry point /
Точка входа приложения.
"""


class Application(QtWidgets.QApplication):

    """
    main application class /
    главный класс приложения
    """

    mode: FORMS
    application_database: connector.ApplicationDatabase
    working_database: connector.Connection
    log_in_attempts: int = 3
    user: actions.User = None
    window: _Window

    def __init__(self, argv: tuple[str]) -> None:

        super().__init__(argv)
        self.window = Window()

        self.theme = theme_switcher
        self.theme.switch_theme("dark")

        self.window.signals.info.connect(self.show_help)
        self.window.signals.button_click.connect(
            lambda name: self._on_button_click(name))

        self.application_database = connector.ApplicationDatabase()

    def run(self) -> int:
        self.window.show()
        # self.authentification()
        self.switch_mode("nofile")
        exit_code = self.exec()
        logger.debug("FINSH")
        return exit_code

    def _on_button_click(self, name: str):
        print(name)
        if name == "file-undo":
            self.theme.switch_theme("light")
        if name == "file-redo":
            self.theme.switch_theme("dark")
        if self.mode == "nofile":
            self._on_button_click_nofile_mode(name)
            return
        else:
            pass

    def _on_button_click_nofile_mode(self, name: str):
        if name == "file-file":
            path = dialogs.getOpenFileDialog("Открыть файл", cfg.APP_DATABASE_PATH)
            print(path)

    def switch_mode(self, mode: FORMS):
        self.mode = mode
        self.window.show_form(mode)
        self.theme.repeat()

    def authentification(self):
        self.switch_mode("auth")
        self.window.forms["auth"].signals.send.connect(
            lambda result: self.log_in(result["login"], result["password"]))

    def log_in(self, login: str, password: str):
        if not login or not password:
            return
        user = self.application_database.log_in(login, password)
        if user:
            self.user = user
            self.log_in_success()
        else:
            self.log_in_failed()
            self.log_in_attempts -= 1

    def log_in_success(self):
        logger.debug("AUTHORIZATION SUCCESS")
        self.switch_mode("nofile")

    def log_in_failed(self):
        if self.log_in_attempts > 0:
            logger.debug("AUTHORIZATION ATTEMPT FAILED")
            self.window.auth_signals.incorrect.emit(self.log_in_attempts)
        else:
            logger.debug("AUTHORIZATION BLOCK")
            self.window.auth_signals.suspicious.emit()

    def show_help(self):
        self.window.show_help(self.mode)
