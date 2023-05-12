from PyQt6 import QtCore

from . import abstract_windows as absw
from . import config as cfg
from .widgets import TextButton
from . import qt_shortcuts as shorts


class Dropdown(absw.AbstractMessage):

    """
    Dropdown menu /
    Выпадающее меню
    """

    def __init__(
            self,
            window: absw.AbstractWindow,
            position: QtCore.QPoint,
            buttons: tuple[TextButton],
            previous: absw.AbstractDialog = None):

        height = sum(b.height() for b in buttons) + 24
        size = QtCore.QSize(200, height)
        geo = QtCore.QRect(position, size)
        absw.AbstractMessage.__init__(self, window, geo, previous)

        layout = shorts.VLayout(self.island)
        layout.addItem(shorts.VSpacer())

        for button in buttons:
            layout.addWidget(button)
        layout.addItem(shorts.VSpacer())
        self.buttons = buttons
