from PyQt6 import QtWidgets, QtSvg, QtCore, QtGui

from . import config as cfg
from . import qt_shortcuts as qts

"""
Module with customized PyQt6 basic widgets /
Модуль с модифицированными базовыми виджетами библиотеки PyQt6

There are widgets with extended functionality and behavour /
Виджеты с расширенным функционалом и поведением

"""


class SvgLabel(QtWidgets.QLabel):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(self, filename:str):

        QtWidgets.QLabel.__init__(self)
        self.setFixedSize(*cfg.BUTTONS_SIZE)
        layout = qts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.set_icon(filename, )

    def set_icon(
            self,
            filename:str,
            color: QtGui.QColor,
            size: QtCore.QSize):
        renderer = QtSvg.QSvgRenderer(f"{cfg.ICONS_PATH}\\{filename}.svg")
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(color))
        renderer.render(painter)
        painter.end()
        self.setPixmap(pixmap)
