import os
from typing import Literal

from PyQt6.QtCore import QSize

"""
Module containing structures, global constants and state variables /
Модуль, содержащий зависимости, структуры данных,
глобальные константы и переменные состояния.

Must be imported by each module /
Должен быть импортирован всеми остальными модулями.
"""

FORMS = Literal["main", "auth", "nofile"]

NARROW_START = 1000

ICONS_SIZE: QSize = QSize(28, 28)
ICONS_BIG_SIZE: QSize = QSize(64, 64)
ICONS_LARGE_SIZE: QSize = QSize(90, 90)
ICONS_PATH = ".\\icons"
FONTS_PATH = ".\\fonts"

BUTTONS_SIZE: QSize = QSize(36, 36)
APP_DATABASE_PATH = ".\\programdata\\database.db"

DATABASE_FINDER_FILTER = "Sqlite3 database (*.db *.sqlite3)"
DATABASE_FINDER_PATH = f"C:\\users\\{os.getlogin()}\\Desktop"

GAP = 8
BORDER_RADUIS = 12
MAIN_FONTSIZE = 12
TEXT_FONTSIZE = 14
HEAD_FONTSIZE = 16


MAIN_FONT_FAMILY = "Ubuntu"
HEAD_FONT_FAMILY = "Montserrat"
MONO_FONT_FAMILY = "Ubuntu_Mono"


THEMES = {
    "light": {
        "theme_icon": "sun",
        "back": (255, 255, 255),
        "fore": (30, 30, 30),
        "highlight1": (225, 225, 225),
        "highlight2": (235, 235, 235),
        "highlight3": (249, 249, 249),
        "dim": (0, 0, 0, 25),
        "red": (255, 61, 61),
        "yellow": (255, 160, 32),
        "green": (32, 213, 32),
        "blue": (36, 138, 255),
        "icons_main_color": "black",
        "icons_alter_color": "white",
    },
    "dark": {
        "theme_icon": "moon",
        "back": (10, 10, 10),
        "fore": (255, 255, 255),
        "highlight1": (40, 40, 40),
        "highlight2": (30, 30, 30),
        "highlight3": (20, 20, 20),
        "dim": (255, 255, 255, 25),
        "red": (255, 61, 61),
        "yellow": (255, 160, 32),
        "green": (32, 213, 32),
        "blue": (36, 138, 255),
        "icons_main_color": "white",
        "icons_alter_color": "black"
    }
}
LANGUAGES = ("ru", "en")
VOCABULARY = (
    ("Авторизация", "Authorization"),
    ("Файл", "File"),
    ("Аккаунт", "Account"),
    ("Мой аккаунт", "My account"),
    ("Пользователи", "Users"),
    ("База данных", "Database"),
    ("История", "History"),
    ("Экспорт", "Eport"),
    ("Статистика", "Statistics"),
    ("Настройки", "Settings"),
    ("Выйти", "Exit"),
    ("Открыть папку", "Open folder"),
    ("Открыть файл", "Open file"),
    ("Сохранить", "Save"),
    ("Отменить", "Undo"),
    ("Повторить", "Redo"),
    ("Фильтр", "Filter"),
    ("Изменение", "Update"),
    ("Удаление", "Delete"),
    ("Добавление", "Add"),
    ("Создать таблицу", "Create table"),
    ("Удалить таблицу", "Drop table"),
    ("Создать столбец", "Add column"),
    ("Удалить столбец", "Drop column"),
    ("Автосохранение", "Autosave"),
    ("Режим работы", "Mode"),
    ("Язык", "Language"),
    ("Тема", "Theme"),
    ("Пароль", "Password"),
    ("Логин", "Login"),
    ("Файл не выбран", "no file"),
    ("Изменений нет", "nothing to commit"),
    ("Не синхронизировано", "out of sync")
)


def icon(color: Literal["black", "white"], name: str) -> str:
    return f"{os.getcwd()}{ICONS_PATH}\\{color}\\{name}.svg"


def radius(size: QSize = BUTTONS_SIZE):
    return int(size.height()/2)

