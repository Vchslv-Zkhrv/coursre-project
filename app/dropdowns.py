from PyQt6 import QtCore

from . import abstract_windows as absw
from .config import GAP
from . import config as cfg
from .widgets import TextButton
from . import shorts


class DropdownButton(TextButton):
    """
    TextButton, but without border-radius and with 8px left and right padding /
    TextButton, только без скругленных углов и с внутренним отступом 8пикс слева и справа
    """

    def __init__(self, icon_name: str, text: str, object_name: str):
        TextButton.__init__(self, icon_name, text, object_name)
        self.layout().setContentsMargins(GAP, 0, GAP, 0)


class Dropdown(absw.AbstractMessage):

    """
    Dropdown menu /
    Выпадающее меню
    """

    def __init__(
            self,
            window: absw.AbstractWindow,
            buttons: tuple[TextButton],
            previous: absw.AbstractDialog = None):

        height = sum(b.height() for b in buttons) + cfg.BORDER_RADUIS*2 + 4
        self.size_ = QtCore.QSize(240, height)
        absw.AbstractMessage.__init__(self, window, previous)

        layout = shorts.VLayout(self.island)
        layout.addItem(shorts.VSpacer())

        for button in buttons:
            layout.addWidget(button)

        layout.addItem(shorts.VSpacer())
        self.buttons = buttons

    def show_(self, position: QtCore.QPoint):
        geo = QtCore.QRect(position, self.size_)
        super().show_(geo)
