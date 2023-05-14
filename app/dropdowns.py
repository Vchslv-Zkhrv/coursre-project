from PyQt6 import QtCore

from . import abstract_windows as absw
from .config import GAP, BORDER_RADUIS
from .widgets import TextButton
from . import shorts
from .personalization import rgba, CURRENT_THEME as THEME


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

        height = sum(b.height() for b in buttons) + BORDER_RADUIS*2
        self.size_ = QtCore.QSize(200, height)
        absw.AbstractMessage.__init__(self, window, previous)

        layout = shorts.VLayout(self.island)
        layout.addItem(shorts.VSpacer())

        for button in buttons:
            layout.addWidget(button)
            button.style_ = (f"""
                    background-color: %s;
                    color: {rgba(THEME['fore'])};
                    border: none;
                    border-radius: 0px;""")
            button.layout().setContentsMargins(GAP, 0, GAP, 0)

        layout.addItem(shorts.VSpacer())
        self.buttons = buttons

    def show_(self, position: QtCore.QPoint):
        geo = QtCore.QRect(position, self.size_)
        super().show_(geo)
