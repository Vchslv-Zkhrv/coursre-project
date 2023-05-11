from typing import Any

from PyQt6 import QtWidgets, QtCore

from .events import FormSignals
from . import widgets
from . import qt_shortcuts as shorts
from . import custom_widgets as custom
from . import config as cfg
from . import gui


class Form(QtWidgets.QFrame):

    """
    Simple frame that can emit "send" signal
    and collect inputed data to a dictionary /
    Простой фрейм, который может испускать сигнал "send"
    и собирать собранные данные в словарь
    """

    inputs: tuple[QtWidgets.QWidget]

    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.signals = FormSignals()

    def collect(self) -> dict[str, str|bool]:
        result = dict()
        for input in self.inputs:
            name = input.objectName()
            value = None
            if isinstance(input, widgets.LineEdit):
                value = input.text()
            if isinstance(input, widgets.PasswordInput):
                value = input.input.text()
            result[name] = value
        return result


class AuthForm(Form):

    """
    Authentification form /
    Форма аутентификации
    """

    def __init__(self):
        Form.__init__(self)
        self.setStyleSheet("""
            border: none;
            color: none;
            background-color: none""")
        self.setFixedSize(250, 300)

        layout = shorts.VLayout(self)
        icon = custom.SvgLabel(
            widgets.icon("black", "circle-person"),
            QtCore.QSize(90, 90))
        title = widgets.Label("Авторизация", gui.main_family.font(17, "Medium"))
        self.login = widgets.LineEdit("Логин")
        self.login.setObjectName("login")
        self.login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password = widgets.PasswordInput()
        self.password.input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setObjectName("password")

        layout.addWidget(icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addItem(shorts.VSpacer())
        wrapper = QtWidgets.QFrame(self)
        wl = shorts.VLayout(wrapper)
        wl.addWidget(self.login)
        wl.addWidget(self.password)
        wl.setSpacing(12)
        layout.addWidget(wrapper)

        self.accept = widgets.ColorButton("arrow-right-circle", cfg.GREEN)
        layout.addItem(shorts.VSpacer())
        layout.addWidget(self.accept, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.inputs = (self.password, self.login)
        self.accept.clicked.connect(lambda e: self.signals.send.emit())
