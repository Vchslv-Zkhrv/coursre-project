from PyQt6 import QtCore

from . import config as cfg
from .widgets import SvgTextButton
from . import shorts
from . import popups
from . import dynamic
from .dynamic import global_widget_manager as gwm


def get_dropdown_button(
        icon_name: str,
        text: str,
        object_name: str,
        shortcut: str) -> SvgTextButton:

    button = SvgTextButton(icon_name, text)
    button.setContentsMargins(cfg.BORDER_RADUIS, 0, cfg.BORDER_RADUIS, 0)
    gwm.add_widget(button, object_name)
    gwm.add_shortcut(object_name, shortcut)
    gwm.set_style(object_name, "always", dynamic.always % 0)
    gwm.set_style(object_name, "leave", "color: !fore!; background-color: !back!;")
    gwm.set_style(object_name, "hover", "color: !fore!; background-color: !highlight2!;")
    return button


class Dropdown(popups.Message):

    """
    Dropdown menu /
    Выпадающее меню
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            buttons: tuple[SvgTextButton],
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
