from PyQt6 import QtWidgets

from .abstract_windows import AbstractWindow
from . import shorts
from . import widgets
from . import events
from .dropdowns import Dropdown
from . import config as cfg
from .config import rgba, GAP, CURRENT_THEME as THEME
from . import custom_widgets as custom
from . import gui

class Group(QtWidgets.QFrame):

    """
    Regular frame without style /
    Обычный фрейм без стиля
    """

    def __init__(self, parent: QtWidgets.QWidget = None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            background-color: none;
            color: none;
            border: none;""")


toolbar_items = tuple[widgets.ShrinkingButton, tuple[widgets.TextButton, str]]


class ToolBar(Group):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    buttons: toolbar_items

    def __init__(self, window: AbstractWindow):
        Group.__init__(self)
        self.signals = events.ToolbarEvents()
        layout = shorts.HLayout(self)
        layout.setSpacing(8)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.window_ = window
        self.buttons = (
            (
                widgets.ShrinkingButton(window, "circle-person", "Профили", 104, "profile"),
                (
                    (widgets.TextButton("user-pen", "Аккаунт", "user-account"), "Ctrl+A"),
                    (widgets.TextButton("user-cross", "Выйти", "user-exit"), "Ctrl+Alt+A"),
                    (widgets.TextButton("users-three", "Профили", "user-accounts"), "Ctrl+Shift+A")
                )
             ),

            (
                widgets.ShrinkingButton(window, "book-bookmark", "Файл", 88, "file"),
                (
                    (widgets.TextButton("folder", "Открыть проект", "file-folder"), "Ctrl+Shift+O"),
                    (widgets.TextButton("document-text", "Открыть файл", "file-file"), "Ctrl+O"),
                    (widgets.TextButton("floppy-disk", "Сохранить", "file-save"), "Ctrl+S"),
                    (widgets.TextButton("share-reverse", "Отменить", "file-undo"), "Ctrl+Z"),
                    (widgets.TextButton("share", "Повторить", "file-redo"), "Ctrl+Shift+Z")
                )
            ),

            (
                widgets.ShrinkingButton(window, "server", "База данных", 122, "database"),
                (
                    (widgets.TextButton("filter", "Фильтр", "database-filter"), "Ctrl+F"),
                    (widgets.TextButton("sticky-note-pen", "Изменение", "database-edit"), "Ctrl+E"),
                    (widgets.TextButton("trash", "Удаление", "database-delete"), "Ctrl+-"),
                    (widgets.TextButton("circle-plus", "Добавление", "database-add"), "Ctrl+="),
                    (widgets.TextButton("square-grid", "+ таблица", "database-create"), "Ctrl+Alt+="),
                    (widgets.TextButton("square", "- таблица", "database-drop"), "Ctrl+Alt+-"),
                    (widgets.TextButton("square-plus", "+ столбец", "database-column"), "Ctrl+Shift+="),
                    (widgets.TextButton("square-minus", "- столбец", "database-alter"), "Ctrl+Shift+-")
                )
            ),

            (
                widgets.ShrinkingButton(window, "share (2)", "Экспорт", 95, "export"),
                (
                )
            ),

            (
                widgets.ShrinkingButton(window, "chart-line", "Статистика", 112, "statistics"),
                (
                )
            ),

            (
                widgets.ShrinkingButton(window, "settings", "Настройки", 113, "settings"),
                (
                    (widgets.TextButton("clock-duration", "Автосохранение", "settings-autosave"), "Ctrl+Alt+S"),
                    (widgets.TextButton("document-check", "Режим работы", "settings-mode"), "Ctrl+`"),
                    (widgets.TextButton("palette", "Тема", "settings-theme"), "Ctrl+T"),
                    (widgets.TextButton("language", "Язык", "settings-language"), "Ctrl+L"),
                )
            )
        )

        self._place_widgets(self.buttons)

    def _place_widgets(self, buttons: toolbar_items):

        for head_button, dropdown_butons in buttons:
            dropdown_butons: tuple[widgets.TextButton, str]
            buttons: tuple[widgets.TextButton] = tuple(db[0] for db in dropdown_butons)

            self.layout().addWidget(head_button)
            self._connect_signal(head_button)
            head_button.clicked.connect(
                lambda e, head=head_button, buttons=buttons:
                self._draw_dropdown(head, buttons)
            )
            for db in buttons:
                self._connect_signal(db)

            for button, hotkey in dropdown_butons:
                button.set_shortcut(hotkey, self.window_)

        self.layout().addItem(shorts.HSpacer())

    def _draw_dropdown(
            self,
            head_button: QtWidgets.QPushButton,
            buttons: tuple[QtWidgets.QPushButton]):
        point = head_button.geometry().bottomLeft()
        point.setX(point.x() + GAP*2)
        point.setY(point.y() + GAP)
        dd = Dropdown(
            self.window_,
            point,
            buttons)
        dd.show()

    def _connect_signal(self, button: QtWidgets.QPushButton):
        button.clicked.connect(
            lambda e, name=button.objectName():
            self.signals.button_clicked.emit(name))


class StatusBar(Group):

    """
        Statusbar for MainWindow /
        Статусбар для главного кона
    """

    def __init__(self, window: AbstractWindow):
        Group.__init__(self)
        self.signals = events.ToolbarEvents()
        self.window_ = window
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['highlight1'])};
            border-radius: {int(self.height()/2)};
            border: none;""")

        layout = shorts.HLayout(self)
        layout.setContentsMargins(int(GAP/2), 0, GAP, 0)
        self.normal_document_icon = custom.SvgLabel(widgets.icon("black", "document"))
        self.unknown_document_icon = custom.SvgLabel(widgets.icon("black", "document-search"))
        self.path = widgets.Label("Файл не выбран", gui.main_family.font())
        self.empty_commit_icon = custom.SvgLabel(widgets.icon("black", "git-commit"))
        self.filled_commit_icon = custom.SvgLabel(widgets.icon("black", "git-commit-filled"))
        self.commit = widgets.Label("Изменений нет", gui.main_family.font())
        self.empty_branch_icon = custom.SvgLabel(widgets.icon("black", "git-branch"))
        self.filled_branch_icon = custom.SvgLabel(widgets.icon("black", "git-branch-filled"))
        self.branch = widgets.Label("Не синронизировано", gui.main_family.font())

        self.path.setStyleSheet(self.styleSheet())
        self.commit.setStyleSheet(self.styleSheet())
        self.branch.setStyleSheet(self.styleSheet())

        layout.addWidget(self.normal_document_icon)
        layout.addWidget(self.unknown_document_icon)
        layout.addWidget(self.path)
        layout.addWidget(shorts.Spacer(width=8))
        layout.addWidget(self.empty_commit_icon)
        layout.addWidget(self.filled_commit_icon)
        layout.addWidget(self.commit)
        layout.addWidget(shorts.Spacer(width=8))
        layout.addWidget(self.empty_branch_icon)
        layout.addWidget(self.filled_branch_icon)
        layout.addWidget(self.branch)

        self.normal_document_icon.hide()
        self.filled_branch_icon.hide()
        self.filled_commit_icon.hide()

    def _set_status(
            self,
            icon0: custom.SvgLabel,
            icon1: custom.SvgLabel,
            label: widgets.Label,
            status: bool,
            message: str):
        
        label.setText(message)
        if status:
            icon1.show()
            icon0.hide()
        else:
            icon1.hide()
            icon0.show()

    def set_commit_status(self, status: bool, message: str):
        return self._set_status(
            self.empty_commit_icon,
            self.filled_commit_icon,
            self.commit,
            status,
            message
        )

    def set_branch_status(self, status: bool, message: str):
        return self._set_status(
            self.empty_branch_icon,
            self.filled_branch_icon,
            self.branch,
            status,
            message
        )

    def set_file_status(self, status: bool, message: str):
        return self._set_status(
            self.unknown_document_icon,
            self.normal_document_icon,
            self.path,
            status,
            message
        )


class SecondToolbar(Group):

    """
    Second toolbar placed under the titlebar /
    Вторая полоса инструментов, расположенная под шапкой окна
    """

    def __init__(self, window: AbstractWindow):
        Group.__init__(self)
        self.window_ = window
        self.signals = events.ToolbarEvents()
        self.signals.button_clicked.connect(lambda name: window._on_toolbar_button_click(name))
        self.setFixedHeight(cfg.BUTTONS_SIZE.height() + GAP)
        self.setSizePolicy(shorts.RowPolicy())

        layout = shorts.HLayout(self)
        layout.setContentsMargins(GAP, GAP, GAP, 0)
        layout.setSpacing(GAP)

        self.status_bar = StatusBar(window)
        layout.addWidget(self.status_bar)

        self.history_button = widgets.ShrinkingButton(
            window,
            "git-compare",
            "История",
            100,
            "history"
        )
        self.history_button.set_shortcut("Ctrl+H", window)
        self.history_button.clicked.connect(lambda e: self.signals.button_clicked.emit("history"))
        layout.addWidget(self.history_button)

        layout.addItem(shorts.HSpacer())
