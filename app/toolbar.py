from . import widgets
from . import shorts
from .dropdowns import Dropdown, get_dropdown_button as dd_button
from .groups import Group
from . import config as cfg
from .config import GAP
from . import dynamic
from .dynamic import global_widget_manager as gwm

class ToolBar(Group):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    buttons: tuple[widgets.TextButton, tuple[widgets.TextButton]]

    def __init__(self, window: dynamic.DynamicWindow):
        Group.__init__(self)
        layout = shorts.HLayout(self)
        layout.setSpacing(8)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.window_ = window

        self.add_button(
            widgets.TextButton("circle-person", "Профили"),
            "toolbar-profile",
            dd_button("user-pen", "Аккаунт", "user-account", "Ctrl+A"),
            dd_button("user-cross", "Выйти", "user-exit", "Ctrl+Alt+A"),
            dd_button("users-three", "Профили", "user-accounts", "Ctrl+Shift+A")
        )
        self.add_button(
            widgets.TextButton("book-bookmark", "Файл"),
            "toolbar-file",
            dd_button("folder", "Открыть проект", "file-folder", "Ctrl+Shift+O"),
            dd_button("document-text", "Открыть файл", "file-file", "Ctrl+O"),
            dd_button("floppy-disk", "Сохранить", "file-save", "Ctrl+S"),
            dd_button("share-reverse", "Отменить", "file-undo", "Ctrl+Z"),
            dd_button("share", "Повторить", "file-redo", "Ctrl+Shift+Z")
        )
        self.add_button(
            widgets.TextButton("server", "База данных"),
            "toolbar-database",
            dd_button("filter", "Фильтр", "database-filter", "Ctrl+F"),
            dd_button("sticky-note-pen", "Изменение", "database-edit", "Ctrl+E"),
            dd_button("trash", "Удаление", "database-delete", "Ctrl+-"),
            dd_button("circle-plus", "Добавление", "database-add", "Ctrl+="),
            dd_button("square-grid", "+ таблица", "database-create", "Ctrl+Alt+="),
            dd_button("square", "- таблица", "database-drop", "Ctrl+Alt+-"),
            dd_button("square-plus", "+ столбец", "database-column", "Ctrl+Shift+="),
            dd_button("square-minus", "- столбец", "database-alter", "Ctrl+Shift+-")
        )
        self.add_button(
            widgets.TextButton("share (2)", "Экспорт"),
            "toolbar-export",
        )
        self.add_button(
            widgets.TextButton("chart-line", "Статистика"),
            "toolbar-statistics",
        )
        self.add_button(
            widgets.TextButton("settings", "Настройки"),
            "toolbar-settings",
            dd_button("clock-duration", "Автосохранение", "settings-autosave", "Ctrl+Alt+S"),
            dd_button("document-check", "Режим работы", "settings-mode", "Ctrl+`"),
            dd_button("palette", "Тема", "settings-theme", "Ctrl+T"),
            dd_button("language", "Язык", "settings-language", "Ctrl+L")
        )

    def add_button(
            self,
            toolbar_button: widgets.TextButton,
            toolbar_button_name: str,
            *dropdown_buttons: widgets.TextButton):

        toolbar_button.setFixedWidth(cfg.BUTTONS_SIZE.width()*3 + GAP)

        self.layout().addWidget(toolbar_button)
        gwm.add_widget(toolbar_button, toolbar_button_name, "button")

        dropdown = Dropdown(
            f"{toolbar_button_name}-dropdown",
            self.window_,
            dropdown_buttons)

        toolbar_button.clicked.connect(
            lambda e: self.show_dropdown(toolbar_button, dropdown))

    def show_dropdown(
            self,
            toolbar_button: widgets.TextButton,
            dropdown: Dropdown):

        pos = toolbar_button.geometry().bottomLeft()
        pos.setX(pos.x() + GAP*2)
        pos.setY(pos.y() + GAP*4)
        dropdown.show_(pos)
