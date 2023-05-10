from typing import Literal

from PyQt6 import QtWidgets, QtGui

from . import custom_widgets as cw
from . import config as cfg
from .config import rgba
from . import events
from . import qt_shortcuts as shorts
from . import gui

"""
Module with final widgets classes / Модуль с классами конечных виджетов.

The classes in this module should be treated as singletons,
but PyQt6 does not allow this pattern /
Классы в этом модуле стоит воспринимать как синглтоны,
однако библиотека PyQt6 не позволяет безопасно применять этот паттерн

"""


def icon(color: Literal["black", "white"], name: str) -> str:
    return f"{cfg.ICONS_PATH}\\{color}\\{name}.svg"


class RegularButton(cw.SvgButton):

    """
    Main button used in application /
    Главная кнопка, используемая в приложении
    """

    def __init__(self, icon_name: str):

        svg0 = svg1 = cw.SvgLabel(icon("black", icon_name))
        c0 = cfg.CURRENT_THEME['back']
        c1 = cfg.CURRENT_THEME['highlight1']

        cw.SvgButton.__init__(self, (svg0, c0), (svg1, c1))


class ColorButton(cw.SvgButton):

    """
    Button switching it's color on hover with icon /
    Кнопка с иконкой, меняющая цвет по наведению
    """

    def __init__(self, icon_name: str, color: QtGui.QColor):

        svg0 = cw.SvgLabel(icon("black", icon_name))
        svg1 = cw.SvgLabel(icon("white", icon_name))
        c0 = cfg.CURRENT_THEME["back"]
        c1 = color

        cw.SvgButton.__init__(self, (svg0, c0), (svg1, c1))


class TextButton(events.HoverableButton):

    """
    Regular button with text and icon /
    Стандартная кнопка с текстом и иконкой
    """

    def __init__(self, icon_name: str, text: str):

        events.HoverableButton.__init__(self)
        self.style_ = f"""
            background-color: %s;
            color: {rgba(cfg.CURRENT_THEME['fore'])};
            border: none;
            border-radius: {int(cfg.BUTTONS_SIZE.height()/2)};"""

        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setStyleSheet(self.style_ % rgba(cfg.CURRENT_THEME["back"]))
        layout = shorts.HLayout(self)
        layout.setSpacing(4)

        svg = cw.SvgLabel(icon("black", icon_name))
        c0 = QtGui.QColor(cfg.CURRENT_THEME["back"])
        c1 = QtGui.QColor(cfg.CURRENT_THEME["highlight1"])
        self.svg = cw.SvgButton((svg, c0), (svg, c1))
        self.layout().addWidget(self.svg)

        self.text_ = events.HoverableButton()
        self.text_.setText(text)
        self.text_.setStyleSheet(self.style_ % "none")
        self.layout().addWidget(self.text_)

        self.text_.setFont(gui.main_family.font())

    def on_hover(self):
        style = self.style_ % rgba(cfg.CURRENT_THEME["highlight1"])
        self.svg.setStyleSheet(style)
        self.setStyleSheet(style)

    def on_leave(self):
        style = self.style_ % rgba(cfg.CURRENT_THEME["back"])
        self.setStyleSheet(style)