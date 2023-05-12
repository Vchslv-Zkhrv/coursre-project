from PyQt6 import QtWidgets, QtCore, QtGui

from .abstract_windows import AbstractWindow
from . import qt_shortcuts as shorts
from . import widgets
from . import events
from .dropdowns import Dropdown
from . import config as cfg


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
        self.window_ = window
        self.buttons = (
            (
                widgets.ShrinkingButton(window, "circle-person", "Профили", 116, "profile"),
                (
                    (widgets.TextButton("user-pen", "Аккаунт", "user-account"), "Ctrl+A"),
                    (widgets.TextButton("user-cross", "Выйти", "user-exit"), "Ctrl+Alt+A"),
                    (widgets.TextButton("users-three", "Профили", "user-accounts"), "Ctrl+Shift+A")
                )
             ),

            (
                widgets.ShrinkingButton(window, "book-bookmark", "Файл", 90, "file"),
                (
                    (widgets.TextButton("folder", "Открыть проект", "file-folder"), "Ctrl+Shift+O"),
                    (widgets.TextButton("document-text", "Открыть файл", "file-file"), "Ctrl+O"),
                    (widgets.TextButton("floppy-disk", "Сохранить", "file-save"), "Ctrl+S"),
                    (widgets.TextButton("share-reverse", "Отменить", "file-undo"), "Ctrl+Z"),
                    (widgets.TextButton("share", "Повторить", "file-redo"), "Ctrl+Shift+Z")
                )
            ),

            (
                widgets.ShrinkingButton(window, "server", "База данных", 137, "database"),
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
                widgets.ShrinkingButton(window, "share (2)", "Экспорт", 108, "export"),
                (
                )
            ),

            (
                widgets.ShrinkingButton(window, "chart-line", "Статистика", 127, "statistics"),
                (
                )
            ),

            (
                widgets.ShrinkingButton(window, "settings", "Настройки", 125, "settings"),
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
        point.setX(point.x() + 16)
        point.setY(point.y() + 8)
        dd = Dropdown(
            self.window_,
            point,
            buttons)
        dd.show()

    def _connect_signal(self, button: QtWidgets.QPushButton):
        button.clicked.connect(
            lambda e, name=button.objectName():
            self.signals.button_clicked.emit(name))
