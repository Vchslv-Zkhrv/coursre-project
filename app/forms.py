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

    children: tuple[QtWidgets.QWidget]

    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.children = ()
        self.signals = FormSignals()

    def collect(self) -> dict[str, Any]:
        result = dict()
        for widget in self.children:
            if isinstance(widget, widgets.LineEdit):
                result[widget.objectName()] = widget.text()
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
        layout = shorts.GLayout(self)

        icon = custom.SvgLabel(
            widgets.icon("black", "circle-person"),
            QtCore.QSize(90, 90))
        title = widgets.Label("Авторизация", gui.main_family.font(17, "Medium"))
        login = widgets.LineEdit("Логин")
        login.setObjectName("login")
        login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        password = widgets.LineEdit("Пароль")
        password.setObjectName("password")
        password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addItem(shorts.HSpacer(), 0, 0, 2, 1)
        layout.addWidget(icon, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 1, 1, 1, 1)
        layout.addItem(shorts.HSpacer(), 0, 2, 2, 1)
        layout.addItem(shorts.VSpacer(), 2, 0, 1, 3)
        wrapper = QtWidgets.QFrame(self)
        wl = shorts.GLayout(wrapper)
        wl.addWidget(login, 0, 0, 1, 1)
        wl.addWidget(password, 1, 0, 1, 1)
        wl.setSpacing(12)
        layout.addWidget(wrapper, 3, 0, 1, 3)

        self.setFixedSize(250, 250)
