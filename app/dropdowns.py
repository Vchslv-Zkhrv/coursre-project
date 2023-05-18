from PyQt6 import QtCore

from .config import GAP
from . import config as cfg
from .widgets import TextButton
from . import shorts
from . import popups
from . import dynamic

class DropdownButton(TextButton):
    """
    TextButton, but without border-radius and with 8px left and right padding /
    TextButton, только без скругленных углов и с внутренним отступом 8пикс слева и справа
    """

    def __init__(
            self,
            object_name: str,
            icon_name: str,
            text: str):

        TextButton.__init__(self, object_name, icon_name, text)
        self.layout().setContentsMargins(GAP, 0, GAP, 0)


class Dropdown(popups.Message):

    """
    Dropdown menu /
    Выпадающее меню
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            buttons: tuple[TextButton],
            previous: popups.Dialog = None):

        height = sum(b.height() for b in buttons) + cfg.BORDER_RADUIS*2 + 4
        self.size_ = QtCore.QSize(240, height)
        popups.Message.__init__(self, object_name, window, previous)

        layout = shorts.VLayout(self.island)
        layout.addItem(shorts.VSpacer())

        for button in buttons:
            layout.addWidget(button)

        layout.addItem(shorts.VSpacer())
        self.buttons = buttons

    def show_(self, position: QtCore.QPoint):
        geo = QtCore.QRect(position, self.size_)
        super().show_(geo)
