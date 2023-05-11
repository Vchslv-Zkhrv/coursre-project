from typing import Literal

from PyQt6 import QtWidgets, QtGui

from . import custom_widgets as cw
from . import config as cfg
from .config import rgba, CURRENT_THEME as THEME
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
        c0 = THEME['back']
        c1 = THEME['highlight1']

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


class Label(QtWidgets.QLabel):

    """
    Simple label widget /
    Простой виджет метки
    """

    def __init__(self, text: str, font: gui.Font):
        QtWidgets.QLabel.__init__(self)
        self.setWordWrap(True)
        self.setText(text)
        self.setFont(font)
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['back'])};
            color: {rgba(THEME['fore'])};
            border: none;""")


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

        self.icon = cw.SvgLabel(icon("black", icon_name), cfg.BUTTONS_SIZE)
        self.label = Label(text, gui.main_family.font())

        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setStyleSheet(self.style_ % rgba(cfg.CURRENT_THEME["back"]))
        self.setSizePolicy(shorts.MinimumPolicy())
        layout = shorts.HLayout(self)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)

        self.signals.hovered.connect(self.on_hover)
        self.signals.leaved.connect(self.on_leave)

    def setStyleSheet(self, styleSheet: str) -> None:
        self.label.setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)

    def on_hover(self):
        self.setStyleSheet(self.style_ % rgba(THEME["highlight1"]))

    def on_leave(self):
        self.setStyleSheet(self.style_ % rgba(THEME["back"]))


class LineEdit(QtWidgets.QLineEdit):

    """
    Simple line input widget /
    Простой виджет ввода строки
    """

    def __init__(self, placeholder: str):
        QtWidgets.QLineEdit.__init__(self)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setStyleSheet(f"""
            background-color: {rgba(THEME['highlight1'])};
            color: {rgba(THEME['fore'])};
            border: none;
            border-radius: {int(self.height()/2)}px;
            padding-right: 8px;
            padding-left: 8px;""")
        self.setFont(gui.main_family.font())


class SwitchingButton(QtWidgets.QFrame):

    """
    Button switching it's icon by click /
    Кнопка, переключающая свою иконку по клику
    """

    icons: tuple[RegularButton]

    def __init__(self, *states: tuple[str, str]):
        QtWidgets.QFrame.__init__(self)
        self.signals = events.SwitchingButtonSignals()
        self.setFixedSize(cfg.BUTTONS_SIZE)
        self.setStyleSheet("""
            background-color: none;
            color: none;
            border: none""")
        layout = shorts.GLayout(self)

        self.icons = tuple(RegularButton(state[0]) for state in states)
        names = tuple(state[1] for state in states)

        for i in range(0, len(states)):
            icon = self.icons[i]
            layout.addWidget(icon, 0, 0, 1, 1)
            if i:
                icon.hide()
            icon.setObjectName(names[i])
            icon.clicked.connect(lambda e, i=i: self.switch(i))

    def switch(self, sender_index: int):
        self.signals.switched.emit()
        self.icons[sender_index].hide()
        self.icons[sender_index - 1].show()

    def selected(self) -> str:
        for icon in self.icons:
            if icon.isVisible():
                return icon.objectName()
