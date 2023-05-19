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
            object_name: str,
            window_: dynamic.DynamicWindow,
            icon_name: str,
            title: str):

        popups.Dialog.__init__(self, object_name, window_)
        layout = shorts.VLayout(self.island)

        self.icon = widgets.SvgLabel(
            icon_name,
            "icons_main_color",
            cfg.ICONS_BIG_SIZE)

        font = gui.main_family.font(HEAD_FONTSIZE, "Medium")
        self.title = widgets.Label(title, font)
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


class AlertDialog(Dialog):

    """
    Dialog with text and exit button /
    Диалог с текстом и кнопкой "выход"
    """

    def __init__(
            self,
            object_name: str,
            window_: dynamic.DynamicWindow,
            description: str):

        Dialog.__init__(self, object_name, window_, "circle-info", "Предупреждение")
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
            object_name: str,
            window_: dynamic.DynamicWindow,
            description: str):

        Dialog.__init__(
            self,
            object_name,
            window_,
            "circle-question",
            "Подтвердите\nдействие")
        self.island.setFixedSize(400, 300)

        self.description = widgets.Label(
            description, gui.main_family.font(size=cfg.TEXT_FONTSIZE))
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.setSizePolicy(shorts.ExpandingPolicy())

        layout = shorts.GLayout(self.body)
        layout.addWidget(self.description, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.no, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.yes, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(GAP*2, GAP*3, GAP*2, 0)
        layout.setVerticalSpacing(GAP*4)
        layout.setHorizontalSpacing(GAP)


class ChooseVariantDialog(Dialog):

    """
    dialog for choosing one of the variants /
    диалог выбора одного из вариантов
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            icon_name: str,
            title: str,
            caption: str,
            *varians: widgets.SvgTextButton):

        Dialog.__init__(self, object_name, window, icon_name, title)

        self.island.setFixedSize(QtCore.QSize(300, 400))

        layout = shorts.VLayout(self.body)
        layout.setContentsMargins(GAP, GAP*3, GAP, GAP)
        layout.setSpacing(GAP*4)

        message: widgets.Label = widgets.Label(caption, gui.main_family.font())
        message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)

        area = widgets.VScrollArea()
        layout.addWidget(area)
        alayout = shorts.VLayout(area.area)
        alayout.setSpacing(GAP)

        for button in varians:
            alayout.addWidget(button)
            button.clicked.connect(lambda e, b=button: self.choice(b.objectName()))

        alayout.addItem(shorts.VSpacer())

    def choice(self, name: str):
        self.accept()


class ChooseFileDialog(ChooseVariantDialog):

    """
    dialog for choosing one file in the set /
    диалог выбора одного файла из множества
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            *files: str):

        variants = []
        for file in files:
            file = os.path.normpath(file)
            short_name = "..." + "\\".join(file.split("\\")[-2:])
            button: widgets.SvgTextButton = widgets.SvgTextButton("document", short_name, file)
            button.label.label.setWordWrap(False)
            variants.append(button)

        ChooseVariantDialog.__init__(
            self,
            object_name,
            window,
            "document-search",
            "Выберите\nфайл",
            "Было найдено несколько файлов.\nВыберите необходимый файл из списка",
            *variants
        )


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
