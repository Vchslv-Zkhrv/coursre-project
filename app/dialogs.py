import os

from PyQt6 import QtWidgets, QtCore

from . import window
from . import qt_shortcuts as shorts
from . import widgets
from . import custom_widgets as cw
from . import config as cfg
from . import gui

"""
Module with completed dialog classes /
Модуль с классами готовых диалогов
"""


class Dialog(window.AbstractDialog):

    """
    Main Dialog template
    """

    def __init__(self, window_: window.AbstractWindow, icon_name: str, title: str):
        window.AbstractDialog.__init__(self, window_)
        layout = shorts.VLayout(self.content)

        self.icon = cw.SvgLabel(
            f"{os.getcwd()}\\{cfg.ICONS_PATH}\\black\\{icon_name}.svg",
            cfg.ICONS_BIG_SIZE)
        font = gui.head_family.font(style="Semibold")
        self.title = widgets.Label(title, font)
        self.exit_button = widgets.ColorButton("cross", cfg.RED)
        self.titlebar = QtWidgets.QFrame()
        self.titlebar.setStyleSheet("""
            background-color: none;
            color: none;
            border:none""")
        self.titlebar.setSizePolicy(shorts.RowPolicy())
        wrapper = QtWidgets.QFrame()
        wl = shorts.GLayout(wrapper)
        layout2 = shorts.HLayout(self.titlebar)
        layout2.setSpacing(12)
        layout2.addWidget(self.icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(self.title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout2.addItem(shorts.HSpacer())
        layout2.addWidget(wrapper, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        wl.addWidget(self.exit_button)
        wl.setContentsMargins(0, 8, 8, 0)
        layout.addWidget(self.titlebar)
        layout.addItem(shorts.VSpacer())
