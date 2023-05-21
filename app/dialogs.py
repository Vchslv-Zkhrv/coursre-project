import os
from typing import Callable

from PyQt6 import QtWidgets, QtCore

from . import shorts
from . import widgets
from . import config as cfg
from .config import GAP, HEAD_FONTSIZE
from . import gui
from . import popups
from . import dynamic
from .dynamic import global_widget_manager as gwm


"""
Module with completed dialog classes /
Модуль с классами готовых диалогов
"""


class Dialog(popups.Dialog):

    """
    Main Dialog template
    """

    def __init__(
            self,
            window_: dynamic.DynamicWindow,
            icon_name: str,
            title: str):

        popups.Dialog.__init__(self, window_)
        layout = shorts.VLayout(self.island)

        self.icon = dynamic.DynamicSvg(
            icon_name,
            "main",
            cfg.ICONS_BIG_SIZE)

        self.title = widgets.Label(
            title,
            gui.main_family.font(HEAD_FONTSIZE, "Medium")
        )
        gwm.add_widget(self.title, style_preset="label")

        self.exit_button = widgets.get_color_button(None, "cross", "red")
        self.exit_button.clicked.connect(lambda e: self.reject())

        self.titlebar = QtWidgets.QFrame()
        self.titlebar.setSizePolicy(shorts.RowPolicy())
        title_layout = shorts.HLayout(self.titlebar)
        title_layout.setSpacing(GAP)
        title_layout.addWidget(self.icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        title_layout.addItem(shorts.HSpacer())
        title_layout.addWidget(self.exit_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.titlebar)
        self.island.setContentsMargins(GAP, GAP, GAP, GAP)

        self.body = QtWidgets.QFrame()
        self.body.setSizePolicy(shorts.ExpandingPolicy())
        layout.addWidget(self.body)

    def show(self) -> None:
        super().show()
        gwm.reload()


class AlertDialog(Dialog):

    """
    Dialog with text and exit button /
    Диалог с текстом и кнопкой "выход"
    """

    def __init__(
            self,
            window_: dynamic.DynamicWindow,
            description: str):

        Dialog.__init__(self, window_, "circle-info", "Предупреждение")
        self.island.setFixedSize(400, 200)
        self.description = widgets.Label(
            description, gui.main_family.font(size=cfg.TEXT_FONTSIZE))
        gwm.add_widget(self.description, None, "label")
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.setSizePolicy(shorts.ExpandingPolicy())
        layout = shorts.GLayout(self.body)
        layout.addWidget(self.description, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(GAP*2, GAP*3, GAP*2, 0)


class YesNoDialog(Dialog):

    """
    Dialog with text and two buttons: deny and accept /
    Диалог с текстом и двумя кнопками: применить и отклонить.
    """

    def __init__(
            self,
            window_: dynamic.DynamicWindow,
            description: str):

        Dialog.__init__(
            self,
            window_,
            "circle-question",
            "Подтвердите\nдействие")

        self.island.setFixedSize(400, 220)

        self.description = widgets.Label(
            description, gui.main_family.font(size=cfg.TEXT_FONTSIZE))
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.setSizePolicy(shorts.ExpandingPolicy())
        gwm.add_widget(self.description, style_preset="label")

        self.yes = widgets.get_color_button(None, "check", "green")
        self.yes.clicked.connect(lambda e: self.accept())
        self.no = widgets.get_color_button(None, "ban", "red")
        self.no.clicked.connect(lambda e: self.reject())

        layout = shorts.GLayout(self.body)
        layout.addWidget(self.description, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.no, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.yes, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(GAP*2, GAP*3, GAP*2, 0)
        layout.setVerticalSpacing(GAP*4)
        layout.setHorizontalSpacing(GAP)


class ChoiceSignals(QtCore.QObject):

    choice = QtCore.pyqtSignal(str)


class ChooseVariantDialog(Dialog):

    """
    dialog for choosing one of the variants /
    диалог выбора одного из вариантов
    """

    variants: dict[str, widgets.SvgTextButton]

    def __init__(
            self,
            window: dynamic.DynamicWindow,
            title: str,
            caption: str):

        Dialog.__init__(self, window, "circle-question", title)
        self.choice_signals = ChoiceSignals()

        self.island.setFixedSize(QtCore.QSize(300, 400))

        layout = shorts.VLayout(self.body)
        layout.setContentsMargins(GAP, GAP*3, GAP, GAP)
        layout.setSpacing(GAP*4)

        self.message = widgets.Label(caption, gui.main_family.font())
        gwm.add_widget(self.message, style_preset="label")
        self.message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message)

        self.area = widgets.VScrollArea()
        layout.addWidget(self.area)
        alayout = shorts.VLayout(self.area.area)
        alayout.setSpacing(GAP)

        self.variants = {}
        self.spacer = shorts.VSpacer()

    def load_variants(self, variants: dict[str, widgets.SvgTextButton]):

        for button in self.variants.values():
            button.hide()
        self.variants = {}

        layout = self.area.area.layout()
        for name, button in variants.items():
            layout.addWidget(button)
            button.clicked.connect(lambda e, n=name: self.choice(n))

        self.variants = variants
        layout.addItem(self.spacer)

    def choice(self, name: str):
        self.choice_signals.choice.emit(name)
        self.accept()


class FilterDialog(Dialog):

    def __init__(self, window: dynamic.DynamicWindow):
        Dialog.__init__(self, window, "filter", "Фильтрация")
        self.setFixedSize(500, 500)


def getPath(
        method: callable,
        caption: str,
        path: str,
        *args) -> str:
    path: str = method(None, caption, path, *args)
    if not path:
        raise FileNotFoundError
    return path


def getSaveFileDialog(
        caption: str,
        path: str,
        filter: str = cfg.DATABASE_FINDER_FILTER) -> str:
    return getPath(QtWidgets.QFileDialog.getSaveFileName, caption, path, filter)[0]


def getOpenFileDialog(
        caption: str,
        path: str,
        filter: str = cfg.DATABASE_FINDER_FILTER) -> str:
    return getPath(QtWidgets.QFileDialog.getOpenFileName, caption, path, filter)[0]


def getExistingFolderDialog(
        caption: str,
        path: str) -> str:
    return getPath(QtWidgets.QFileDialog.getExistingDirectory, caption, path)


def recursive_search(start: str, pattern: Callable) -> list[str]:
    result = []

    def path(name):
        return f"{start}\\{name}"

    for _, dirs, files in os.walk(start):
        result.extend(filter(pattern, (path(file) for file in files)))

        for folder in dirs:
            result.extend(recursive_search(path(folder), pattern))

        return result


def getFilesFromFolderDialog(
        caption: str,
        path: str,
        extensions: tuple[str]) -> tuple[str]:

    result = []
    folder = getExistingFolderDialog(caption, path)

    for ext in extensions:
        result.extend(
            recursive_search(
                folder,
                lambda name, ext=ext: name.endswith(ext)
            )
        )

    return tuple(result)
