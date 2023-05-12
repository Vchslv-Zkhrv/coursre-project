from typing import Literal

from PyQt6 import QtWidgets, QtGui, QtCore

from . import custom_widgets as cw
from . import config as cfg
from .config import rgba, CURRENT_THEME as THEME
from . import events
from . import shorts
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
        c1 = THEME['highlight2']

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

    def __init__(self, icon_name: str, text: str, object_name: str):

        events.HoverableButton.__init__(self)
        self.style_ = f"""
            background-color: %s;
            color: {rgba(cfg.CURRENT_THEME['fore'])};
            border: none;
            border-radius: {int(cfg.BUTTONS_SIZE.height()/2)};"""

        self.icon_ = cw.SvgLabel(icon("black", icon_name), cfg.BUTTONS_SIZE)
        self.label = Label(text, gui.main_family.font())

        self.setObjectName(object_name)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setStyleSheet(self.style_ % rgba(cfg.CURRENT_THEME["back"]))
        layout = shorts.HLayout(self)
        layout.addWidget(self.icon_)
        layout.addWidget(self.label)
        layout.setSpacing(2)

        self.signals.hovered.connect(self.on_hover)
        self.signals.leaved.connect(self.on_leave)

    def setStyleSheet(self, styleSheet: str) -> None:
        self.label.setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)

    def on_hover(self):
        self.setStyleSheet(self.style_ % rgba(THEME["highlight2"]))

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
            background-color: {rgba(THEME['highlight2'])};
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


class PasswordInput(QtWidgets.QFrame):

    """
    LineEdit with switching text visility /
    LineEdit с переключаемой видимостью текста
    """

    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.input = LineEdit("Пароль")

        layout = shorts.GLayout(self)
        self.eye = SwitchingButton(
            ("eye", "show password"),
            ("eye-slash", "hide password")
        )
        for icon in self.eye.icons:
            icon.state0 = (icon.state0[0], icon.state1[1])
            icon._set_state(icon.state0)
        self.eye.signals.switched.connect(self.hide_password)
        self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(self.input, 0, 0, 1, 1)
        layout.addWidget(self.eye, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)

    def hide_password(self):
        if self.eye.selected() == "hide password":
            self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        else:
            self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)


class ShrinkingButton(TextButton):

    """
    Button that hides text in response to Window.signals.narrow signal /
    Кнопка, скрывающая текст в ответ на сигнал Window.signals.narrow
    """

    def __init__(self, window, icon_name: str, text: str, width: int, object_name: str):
        TextButton.__init__(self, icon_name, text, object_name)
        self.normal_width = width
        window.signals.narrow.connect(self.shrink)
        window.signals.normal.connect(self.expand)
        if window._is_narrow:
            self.shrink()

    def shrink(self):
        self.label.hide()
        self.setFixedWidth(cfg.BUTTONS_SIZE.width())

    def expand(self):
        self.label.show()
        self.setFixedWidth(self.normal_width)
