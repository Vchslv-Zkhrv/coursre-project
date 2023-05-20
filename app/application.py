import os
from typing import Literal

from PyQt6 import QtWidgets
from loguru import logger

from .windows import Window
from . import connector
from . import actions
from . import dialogs
from . import config as cfg
from .dynamic import global_widget_manager as gwm
from .dropdowns import Dropdown
from . import widgets


"""
Application entry point /
Точка входа приложения.
"""


class Reject(Exception):
    pass


app_mode = Literal[
    "main",
    "nofile",
    "auth",
    "open"
]


class Application(QtWidgets.QApplication):

    """
    main application class /
    главный класс приложения
    """

    mode: app_mode
    application_database: connector.ApplicationDatabase
    working_database: connector.Connection
    log_in_attempts: int = 3
    user: actions.User = None
    window: Window

    def __init__(self, argv: tuple[str]) -> None:

        super().__init__(argv)
        self.window = Window("main window")
        self.window.window_signals.log_in.connect(
            lambda login, password: self.log_in(login, password))
        gwm.add_widget(self.window, "main window", "window")
        gwm.add_hook(
            self._on_dropdown_button_click,
            "click",
            lambda widget: (
                isinstance(widget.window(), Dropdown) and
                isinstance(widget, widgets.SvgTextButton)
            )
        )
        self.application_database = connector.ApplicationDatabase()

    def run(self) -> int:
        self.window.show()
        self.authentification()
        # self.user = connector.User(
        #     "slavic",
        #     "owner",
        #     "C:\\Users\\Slavic\\Desktop\\Новая папка\\database1.db")
        # self.switch_mode("nofile")
        exit_code = self.exec()
        logger.debug("FINSH")
        return exit_code

    def _on_dropdown_button_click(self, name: str):

        action = name.split("-")[1]

        if (
            action in ("file", "folder", "last") and
            self.mode not in ("auth", "open")
        ):
            self._open(action)

    def _open(self, target: Literal["file", "folder", "last"]) -> None:
        old_mode = self.mode[:]
        self.mode = "open"
        try:
            return {
                "file": self._open_file,
                "folder": self._open_folder,
                "last": self._open_last
            }[target]()
        except Reject:
            self.mode = old_mode

    def _open_file(self) -> None:
        path = dialogs.getOpenFileDialog(
            "Открыть файл", cfg.DATABASE_FINDER_PATH)
        if not path:
            raise Reject
        self.connect_database(path)

    def _open_folder(self) -> None:
        paths = dialogs.getFilesFromFolderDialog(
            "Открыть папку проекта",
            cfg.DATABASE_FINDER_PATH,
            (".db", ".sqlite3")
        )
        if len(paths) > 1:
            d = dialogs.ChooseFileDialog(self.window, *paths)
            d.choice_signals.choice.connect(lambda name: self.connect_database(name))
            d.show()
        else:
            raise Reject

    def _open_last(self) -> None:
        if self.user.last_proj and os.path.isfile(self.user.last_proj):
            self.connect_database(self.user.last_proj)
        else:
            raise Reject

    def switch_table(self, index: int):
        if self.mode != "main":
            return
        form = self.window.forms["main"]
        tablename = form.nav.radios[index].text()
        form.table.draw_table(tablename)

    def connect_database(self, path: str):
        if not path:
            return
        try:
            self.working_database = connector.SQL(path)
        except PermissionError:
            d = dialogs.AlertDialog(
                "database permission",
                self,
                "Доступ к базе данных ограничен")
            d.show()
        else:
            self.application_database.update_last_proj(self.user, path)
            self.switch_mode("main")
            self.connect_table(self.working_database)

    def connect_table(self, database: connector.SQL):
        form = self.window.forms["main"]
        form.table.connect(database)
        tablenames = tuple(table.name for table in database.tables.values())
        form.nav.fill(tablenames)

    def switch_mode(self, mode: str):
        self.mode = mode
        self.window.show_form(mode)

    def authentification(self):
        self.switch_mode("auth")

    def log_in(self, login: str, password: str):
        if not login or not password:
            return
        if self.mode != "auth":
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
            self.window._show_log_in_error(self.log_in_attempts)
        else:
            logger.debug("AUTHORIZATION BLOCK")
            self.window._show_suspisious_error()

    def show_help(self):
        self.window.show_help(self.mode)
