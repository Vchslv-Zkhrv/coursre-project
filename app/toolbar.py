from dataclasses import dataclass

from PyQt6 import QtWidgets

from . import widgets
from . import shorts
from .dropdowns import Dropdown
from .abstract_windows import AbstractWindow
from . import events
from .groups import Group
from . import config as cfg
from .config import GAP


class ToolbarButton(widgets.ShrinkingButton):

    """
    Button with dropdown shown by click /
    Кнопка с выпадающим меню, отображаемая по клику
    """

    def __init__(
            self,
            window: AbstractWindow,
            icon_name: str,
            text: str,
            width: int,
            object_name: str,
            buttons: tuple[widgets.TextButton]
            ):

        widgets.ShrinkingButton.__init__(
            self,
            window,
            icon_name,
            text,
            width,
            object_name
        )

        self.dropdown = Dropdown(window, buttons)
        self.clicked.connect(lambda e: self._show_dropdown())

    def _show_dropdown(self):
        pos = self.geometry().bottomLeft()
        pos.setX(pos.x() + GAP*2)
        pos.setY(pos.y() + GAP)
        self.dropdown.show_(pos)


@dataclass
class DropdowItem():

    button: widgets.TextButton
    hotkey: str


@dataclass
class ToolbarItem():

    icon_name: str
    text: str
    width: int
    object_name: str
    buttons: tuple[DropdowItem]


class ToolBar(Group):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    buttons: tuple[ToolbarButton, tuple[widgets.TextButton]]

    def __init__(self, window: AbstractWindow):
        Group.__init__(self)
        self.signals = events.ToolbarEvents()
        layout = shorts.HLayout(self)
        layout.setSpacing(8)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.window_ = window

        buttons = (
            ToolbarItem(
                "circle-person",
                "Профили",
                104,
                "profile",
                (
                    DropdowItem(
                        widgets.TextButton("user-pen", "Аккаунт", "user-account"),
                        "Ctrl+A"
                    ),
                    DropdowItem(
                        widgets.TextButton("user-cross", "Выйти", "user-exit"),
                        "Ctrl+Alt+A"
                    ),
                    DropdowItem(
                        widgets.TextButton("users-three", "Профили", "user-accounts"),
                        "Ctrl+Shift+A"
                    )
                )
             ),

            ToolbarItem(
                "book-bookmark",
                "Файл",
                88,
                "file",
                (
                    DropdowItem(
                        widgets.TextButton("folder", "Открыть проект", "file-folder"),
                        "Ctrl+Shift+O"
                    ),
                    DropdowItem(
                        widgets.TextButton("document-text", "Открыть файл", "file-file"),
                        "Ctrl+O"
                    ),
                    DropdowItem(
                        widgets.TextButton("floppy-disk", "Сохранить", "file-save"),
                        "Ctrl+S"
                    ),
                    DropdowItem(
                        widgets.TextButton("share-reverse", "Отменить", "file-undo"),
                        "Ctrl+Z"
                    ),
                    DropdowItem(
                        widgets.TextButton("share", "Повторить", "file-redo"),
                        "Ctrl+Shift+Z"
                    )
                )
            ),

            ToolbarItem(
                "server",
                "База данных",
                122,
                "database",
                (
                    DropdowItem(
                        widgets.TextButton("filter", "Фильтр", "database-filter"),
                        "Ctrl+F"
                    ),
                    DropdowItem(
                        widgets.TextButton("sticky-note-pen", "Изменение", "database-edit"),
                        "Ctrl+E"
                    ),
                    DropdowItem(
                        widgets.TextButton("trash", "Удаление", "database-delete"),
                        "Ctrl+-"
                    ),
                    DropdowItem(
                        widgets.TextButton("circle-plus", "Добавление", "database-add"),
                        "Ctrl+="
                    ),
                    DropdowItem(
                        widgets.TextButton("square-grid", "+ таблица", "database-create"),
                        "Ctrl+Alt+="
                    ),
                    DropdowItem(
                        widgets.TextButton("square", "- таблица", "database-drop"),
                        "Ctrl+Alt+-"
                    ),
                    DropdowItem(
                        widgets.TextButton("square-plus", "+ столбец", "database-column"),
                        "Ctrl+Shift+="
                    ),
                    DropdowItem(
                        widgets.TextButton("square-minus", "- столбец", "database-alter"),
                        "Ctrl+Shift+-"
                    )
                )
            ),

            ToolbarItem(
                "share (2)",
                "Экспорт",
                95,
                "export",
                (
                )
            ),

            ToolbarItem(
                "chart-line",
                "Статистика",
                112,
                "statistics",
                (
                )
            ),

            ToolbarItem(
                "settings",
                "Настройки",
                113,
                "settings",
                (
                    DropdowItem(
                        widgets.TextButton("clock-duration", "Автосохранение", "settings-autosave"),
                        "Ctrl+Alt+S"
                    ),
                    DropdowItem(
                        widgets.TextButton("document-check", "Режим работы", "settings-mode"),
                        "Ctrl+`"
                    ),
                    DropdowItem(
                        widgets.TextButton("palette", "Тема", "settings-theme"),
                        "Ctrl+T"
                    ),
                    DropdowItem(
                        widgets.TextButton("language", "Язык", "settings-language"),
                        "Ctrl+L"
                    ),
                )
            )
        )

        self._place_widgets(buttons)

    def _connect_signal(self, button: QtWidgets.QPushButton):
        button.clicked.connect(
            lambda e, name=button.objectName():
            self.signals.button_clicked.emit(name))

    def _place_widgets(self, buttons: tuple[ToolbarItem]):

        for item in buttons:
            for button in item.buttons:
                button.button.set_shortcut(button.hotkey, self.window_)
                self._connect_signal(button.button)

            tool = ToolbarButton(
                self.window_,
                item.icon_name,
                item.text,
                item.width,
                item.object_name,
                tuple(b.button for b in item.buttons)
            )

            self._connect_signal(tool)
            self.layout().addWidget(tool)

        self.layout().addItem(shorts.HSpacer())
