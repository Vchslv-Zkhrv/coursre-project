from dataclasses import dataclass

from . import widgets
from . import shorts
from .dropdowns import Dropdown, DropdownButton
from .groups import Group
from . import config as cfg
from .config import GAP
from . import dynamic


class ToolbarButton(widgets.ShrinkingButton):

    """
    Button with dropdown shown by click /
    Кнопка с выпадающим меню, отображаемая по клику
    """

    def __init__(
            self,
            window: dynamic.DynamicWindow,
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
class DropdownItem():

    button: widgets.TextButton
    hotkey: str


@dataclass
class ToolbarItem():

    icon_name: str
    text: str
    width: int
    object_name: str
    buttons: tuple[DropdownItem]


class ToolBar(Group):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    buttons: tuple[ToolbarButton, tuple[widgets.TextButton]]

    def __init__(self, window: dynamic.DynamicWindow):
        Group.__init__(self, "toolbar")
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
                    DropdownItem(
                        DropdownButton("user-pen", "Аккаунт", "user-account"),
                        "Ctrl+A"
                    ),
                    DropdownItem(
                        DropdownButton("user-cross", "Выйти", "user-exit"),
                        "Ctrl+Alt+A"
                    ),
                    DropdownItem(
                        DropdownButton("users-three", "Профили", "user-accounts"),
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
                    DropdownItem(
                        DropdownButton("folder", "Открыть проект", "file-folder"),
                        "Ctrl+Shift+O"
                    ),
                    DropdownItem(
                        DropdownButton("document-text", "Открыть файл", "file-file"),
                        "Ctrl+O"
                    ),
                    DropdownItem(
                        DropdownButton("floppy-disk", "Сохранить", "file-save"),
                        "Ctrl+S"
                    ),
                    DropdownItem(
                        DropdownButton("share-reverse", "Отменить", "file-undo"),
                        "Ctrl+Z"
                    ),
                    DropdownItem(
                        DropdownButton("share", "Повторить", "file-redo"),
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
                    DropdownItem(
                        DropdownButton("filter", "Фильтр", "database-filter"),
                        "Ctrl+F"
                    ),
                    DropdownItem(
                        DropdownButton("sticky-note-pen", "Изменение", "database-edit"),
                        "Ctrl+E"
                    ),
                    DropdownItem(
                        DropdownButton("trash", "Удаление", "database-delete"),
                        "Ctrl+-"
                    ),
                    DropdownItem(
                        DropdownButton("circle-plus", "Добавление", "database-add"),
                        "Ctrl+="
                    ),
                    DropdownItem(
                        DropdownButton("square-grid", "+ таблица", "database-create"),
                        "Ctrl+Alt+="
                    ),
                    DropdownItem(
                        DropdownButton("square", "- таблица", "database-drop"),
                        "Ctrl+Alt+-"
                    ),
                    DropdownItem(
                        DropdownButton("square-plus", "+ столбец", "database-column"),
                        "Ctrl+Shift+="
                    ),
                    DropdownItem(
                        DropdownButton("square-minus", "- столбец", "database-alter"),
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
                    DropdownItem(
                        DropdownButton("clock-duration", "Автосохранение", "settings-autosave"),
                        "Ctrl+Alt+S"
                    ),
                    DropdownItem(
                        DropdownButton("document-check", "Режим работы", "settings-mode"),
                        "Ctrl+`"
                    ),
                    DropdownItem(
                        DropdownButton("palette", "Тема", "settings-theme"),
                        "Ctrl+T"
                    ),
                    DropdownItem(
                        DropdownButton("language", "Язык", "settings-language"),
                        "Ctrl+L"
                    ),
                )
            )
        )

        self._place_widgets(buttons)

    def _connect_signal(self, button: widgets.TextButton):
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
