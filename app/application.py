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
from . import widgets


"""
Top - level logic module /
Модуль с логикой верхнего уровня.
"""


# режимы работы приложения
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
        # конструктор суперкласса 
        QtWidgets.QApplication.__init__(self, argv)
        # отрисовка главного окна и его виджетов
        self._create_window()
        gwm.start()
        # подключение к базе данных приложения
        self.application_database = connector.ApplicationDatabase()

    def _create_window(self) -> None:

        # создание окна
        self.window = Window("main window")
        gwm.add_widget(self.window, "main window", "window")

        # подключение к сигналам окна
        self.window.window_signals.log_in.connect(
            lambda login, password: self.log_in(login, password))
        gwm.add_hook(
            self._on_dropdown_button_click,
            "click",
            lambda widget: (isinstance(widget, widgets.SvgTextButton))
        )
        self.window.signals.triggered.connect(
            lambda trigger: self._window_triggered(trigger))

    def run(self) -> int:
        """
        Launches application and waits for exit.
        Returns application exit code /
        Запускает приложение и ждет завершения.
        Возвращает код завеешения.
        """
        self.window.show()
        # self.authentification()
        self.user = connector.User(
            "slavic",
            "owner",
            "C:\\Users\\Slavic\\Desktop\\Новая папка\\database1.db")
        self.switch_mode("nofile")
        return self.exec()

    def _on_dropdown_button_click(self, name: str):

        print(name)
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
            }[target](old_mode)
        except FileNotFoundError:
            self.mode = old_mode

    def _open_file(self, old_mode: app_mode) -> None:
        path = dialogs.getOpenFileDialog(
            "Открыть файл", cfg.DATABASE_FINDER_PATH)
        if not path:
            self.mode = old_mode
        self.connect_database(path)

    def _open_folder(self, old_mode: app_mode) -> None:
        paths = dialogs.getFilesFromFolderDialog(
            "Открыть папку проекта",
            cfg.DATABASE_FINDER_PATH,
            (".db", ".sqlite3")
        )
        if len(paths) > 1:
            self._open_one(old_mode, paths)
        elif len(paths) == 1:
            self.connect_database(paths[0])
        else:
            self.mode = old_mode

    def _open_one(self, old_mode: app_mode, paths: tuple[str]) -> None:

        variants = {}
        for path in paths:
            path = os.path.normpath(path)
            variants[path] = "..." + "\\".join(path.split("\\")[-2:])

        self.window.show_choice_dialog(
            "Выберите файл",
            "В указанной папке было найдено несколько файлов.\nВыберите один из списка.",
            self.connect_database,
            variants,
            "document"
        )
        self.window.dialogs["choice"].rejected.connect(
            lambda: self.switch_mode(old_mode))

    def _open_last(self, old_mode: app_mode) -> None:
        if self.user.last_proj and os.path.isfile(self.user.last_proj):
            self.connect_database(self.user.last_proj)
        else:
            self.mode = old_mode

    def switch_table(self, tablename: str):
        if self.mode != "main":
            return
        self.window.forms["main"].table.draw_table(tablename)

    def connect_database(self, path: str):
        if not path:
            return
        try:
            self.working_database = connector.SQL(path)
        except PermissionError:
            self.window.show_alert_dialog(
                "Ошибка",
                "Доступ к базе данных ограничен"
            )
        else:
            self.application_database.update_last_proj(self.user, path)
            self.switch_mode("main")
            self.connect_table(self.working_database)
            self.switch_table(self.window.forms["main"].nav.radios[0].text())

    def _on_tablename_click(self, index: int):
        tablename = self.window.forms["main"].nav.radios[index].text()
        return self.switch_table(tablename)

    def connect_table(self, database: connector.SQL):
        form = self.window.forms["main"]
        form.table.connect(database)
        tablenames = tuple(table.name for table in database.tables.values())
        form.nav.fill(tablenames)
        form.nav.radio_signals.item_state_changed.connect(
            lambda index, state: self._on_tablename_click(index)
        )

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
            logger.error("AUTHORIZATION ATTEMPT FAILED")
            self.window.show_log_in_error(self.log_in_attempts)
        else:
            logger.error("AUTHORIZATION BLOCK")
            self.window.show_suspisious_error()

    def show_help(self):
        self.window.show_help(self.mode)

    def _window_triggered(self, trigger: str):
        if trigger == "info":
            self.show_help()
