from PyQt6 import QtWidgets

from .abstract_windows import AbstractWindow
from . import qt_shortcuts as shorts
from . import widgets
from . import events
from .dropdowns import Dropdown


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


toolbar_items = tuple[widgets.ShrinkingButton, tuple[widgets.TextButton]]


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
                    widgets.TextButton("user-pen", "Аккаунт", "user-account"),
                    widgets.TextButton("user-cross", "Выйти", "user-exit"),
                    widgets.TextButton("users-three", "Профили", "user-accounts")
                )
             ),

            (
                widgets.ShrinkingButton(window, "book-bookmark", "Файл", 90, "file"),
                (
                    widgets.TextButton("folder", "Открыть проект", "file-folder"),
                    widgets.TextButton("document-text", "Открыть файл", "file-file"),
                    widgets.TextButton("floppy-disk", "Сохранить", "file-save"),
                    widgets.TextButton("share-reverse", "Отменить", "file-undo"),
                    widgets.TextButton("share", "Повторить", "file-redo")
                )
            ),

            (
                widgets.ShrinkingButton(window, "server", "База данных", 137, "database"),
                (
                    widgets.TextButton("filter", "Фильтр", "database-filter"),
                    widgets.TextButton("sticky-note-pen", "Изменение", "database-edit"),
                    widgets.TextButton("trash", "Удаление", "database-delete"),
                    widgets.TextButton("circle-plus", "Добавление", "database-add"),
                    widgets.TextButton("square-grid", "+ таблица", "database-create"),
                    widgets.TextButton("square", "- таблица", "database-drop"),
                    widgets.TextButton("square-plus", "+ столбец", "database-column"),
                    widgets.TextButton("square-minus", "- столбец", "database-alter")
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
                    widgets.TextButton("clock-duration", "Автосохранение", "settings-autosave"),
                    widgets.TextButton("document-check", "Режим работы", "settings-mode"),
                    widgets.TextButton("palette", "Тема", "settings-theme"),
                    widgets.TextButton("language", "Язык", "settings-language"),
                )
            )
        )

        self._place_widgets(self.buttons)

    def _place_widgets(self, buttons: toolbar_items):

        for head_button, dropdown_butons in buttons:
            self.layout().addWidget(head_button)
            self._connect_signal(head_button)
            head_button.clicked.connect(
                lambda e, head=head_button, buttons=dropdown_butons:
                self._draw_dropdown(head, buttons)
            )
            for db in dropdown_butons:
                self._connect_signal(db)

        self.layout().addItem(shorts.HSpacer())

    def _draw_dropdown(
            self,
            head_button: QtWidgets.QPushButton,
            buttons: tuple[QtWidgets.QPushButton]):
        point = head_button.geometry().bottomLeft()
        point.setX(point.x() + 10)
        dd = Dropdown(
            self.window_,
            point,
            buttons)
        dd.show()

    def _connect_signal(self, button: QtWidgets.QPushButton):
        button.clicked.connect(
            lambda e, name=button.objectName():
            self.signals.button_clicked.emit(name))
