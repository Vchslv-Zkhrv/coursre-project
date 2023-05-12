from PyQt6 import QtWidgets

from .abstract_windows import AbstractWindow
from . import qt_shortcuts as shorts
from . import widgets


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


class ToolBar(Group):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    def __init__(self, window: AbstractWindow):
        Group.__init__(self)
        layout = shorts.HLayout(self)
        layout.setSpacing(8)

        self.profile = widgets.ShrinkingButton(
            window,
            "circle-person",
            "Профили",
            116,
        )

        self.file = widgets.ShrinkingButton(
            window,
            "book-bookmark",
            "Файл",
            90
        )

        self.database = widgets.ShrinkingButton(
            window,
            "server",
            "База данных",
            137
        )

        self.export = widgets.ShrinkingButton(
            window,
            "share",
            "Экспорт",
            108
        )

        self.statistics = widgets.ShrinkingButton(
            window,
            "chart-line",
            "Статистика",
            127
        )

        self.settings = widgets.ShrinkingButton(
            window,
            "settings",
            "Настройки",
            125
        )

        buttons = (
            self.profile,
            self.file,
            self.database,
            self.export,
            self.statistics,
            self.settings
        )

        for button in buttons:
            layout.addWidget(button)

        layout.addItem(shorts.HSpacer())
