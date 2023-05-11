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
        self.setFixedSize(350, 250)

        layout = shorts.GLayout(self)

        icon = custom.SvgLabel(
            widgets.icon("black", "circle-person"),
            QtCore.QSize(90, 90))
        title = widgets.Label("Авторизация", gui.main_family.font(17, "Medium"))
        self.login = widgets.LineEdit("Логин")
        self.login.setObjectName("login")
        self.login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password = widgets.LineEdit("Пароль")
        self.password.setObjectName("password")
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setSizePolicy(shorts.RowPolicy())
        self.eye = widgets.SwitchingButton(
            ("eye", "show password"),
            ("eye-slash", "hide password")
        )
        self.eye.signals.switched.connect(self.hide_password)

        layout.addItem(shorts.HSpacer(), 0, 0, 2, 1)
        layout.addWidget(icon, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 1, 1, 1, 1)
        layout.addItem(shorts.HSpacer(), 0, 2, 2, 1)
        layout.addItem(shorts.VSpacer(), 2, 0, 1, 3)
        wrapper = QtWidgets.QFrame(self)
        wl = shorts.GLayout(wrapper)
        wl.addWidget(self.login, 0, 0, 1, 1)
        wl.addWidget(self.password, 1, 0, 1, 1)
        wl.addWidget(self.eye, 1, 1, 1, 1)
        wl.setSpacing(12)
        layout.addWidget(wrapper, 3, 0, 1, 3)


    def hide_password(self):
        if self.eye.selected() == "hide password":
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
