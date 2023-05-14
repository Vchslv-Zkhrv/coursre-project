from PyQt6 import QtWidgets, QtCore

from .abstract_windows import AbstractDialog, AbstractWindow
from . import shorts
from . import widgets
from . import custom_widgets as custom
from . import config as cfg
from .config import GAP, HEAD_FONTSIZE
from . import gui


"""
Module with completed dialog classes /
Модуль с классами готовых диалогов
"""


class Dialog(AbstractDialog):

    """
    Main Dialog template
    """

    def __init__(
            self,
            name: str,
            window_: AbstractWindow,
            icon_name: str,
            title: str):

        AbstractDialog.__init__(self, name, window_)
        layout = shorts.VLayout(self.island)

        self.icon = custom.SvgLabel(
            icon_name,
            "icons_main_color",
            cfg.ICONS_BIG_SIZE)

        font = gui.main_family.font(HEAD_FONTSIZE, "Medium")
        self.title = widgets.Label(title, font)
        self.exit_button = custom.getColorButton("cross", "red")
        self.titlebar = QtWidgets.QFrame()
        self.titlebar.setSizePolicy(shorts.RowPolicy())
        layout2 = shorts.HLayout(self.titlebar)
        layout2.setSpacing(GAP)
        layout2.addWidget(self.icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(self.title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout2.addItem(shorts.HSpacer())
        layout2.addWidget(self.exit_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.titlebar)
        self.island.setContentsMargins(GAP, GAP, GAP, GAP)

        self.body = QtWidgets.QFrame()
        self.body.setSizePolicy(shorts.ExpandingPolicy())
        layout.addWidget(self.body)

        self.exit_button.clicked.connect(lambda e: self.reject())


class AlertDialog(Dialog):

    """
    Dialog with text and exit button /
    Диалог с текстом и кнопкой "выход"
    """

    def __init__(self, name: str, window_: AbstractWindow, description: str):
        Dialog.__init__(self, name, window_, "circle-info", "Предупреждение")
        self.island.setFixedSize(400, 200)
        self.description = widgets.Label(
            description, gui.main_family.font(size=cfg.TEXT_FONTSIZE))
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
            name: str,
            window_: AbstractWindow,
            description: str):

        Dialog.__init__(self, name, window_, "circle-question", "Подтвердите\nдействие")
        self.island.setFixedSize(400, 300)

        self.description = widgets.Label(
            description, gui.main_family.font(size=cfg.TEXT_FONTSIZE))
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.setSizePolicy(shorts.ExpandingPolicy())
        self.yes = custom.getColorButton("check", "green")
        self.no = custom.getColorButton("ban", "red")

        layout = shorts.GLayout(self.body)
        layout.addWidget(self.description, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.no, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.yes, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(GAP*2, GAP*3, GAP*2, 0)
        layout.setVerticalSpacing(GAP*4)
        layout.setHorizontalSpacing(GAP)

        self.no.clicked.connect(lambda e: self.reject())
        self.yes.clicked.connect(lambda e: self.accept())


def getPath(
        method: callable,
        caption: str,
        path: str,
        *args) -> str:
    return method(None, caption, path, *args)[0]


def getSaveFileDialog(
        caption: str,
        path: str,
        filter: str = cfg.DATABASE_FINDER_FILTER) -> str:
    return getPath(QtWidgets.QFileDialog.getSaveFileName, caption, path, filter)


def getOpenFileDialog(
        caption: str,
        path: str,
        filter: str = cfg.DATABASE_FINDER_FILTER) -> str:
    return getPath(QtWidgets.QFileDialog.getOpenFileName, caption, path, filter)


def getExistingFolderDialog(
        caption: str,
        path: str) -> str:
    return getPath(QtWidgets.QFileDialog.getExistingDirectory, caption, path)
