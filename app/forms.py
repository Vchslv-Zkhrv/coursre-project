from PyQt6 import QtWidgets, QtCore

from . import widgets
from . import shorts
from .config import GAP
from . import gui
from . import tables
from . import dynamic


class Form(dynamic.DynamicFrame):

    """
    Simple frame that can emit "send" signal
    and collect inputed data to a dictionary /
    Простой фрейм, который может испускать сигнал "send"
    и собирать собранные данные в словарь
    """

    inputs: tuple[QtWidgets.QWidget]

    def __init__(self, object_name: str):
        dynamic.DynamicFrame.__init__(self, object_name)

    def collect(self) -> dict[str, str | bool]:
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
        Form.__init__(self, "auth form")
        self.setStyleSheet("""
            border: none;
            color: none;
            background-color: none""")
        self.setFixedSize(250, 300)

        layout = shorts.VLayout(self)

        icon = widgets.SvgLabel(
            "auth-icon",
            "circle-person",
            "icons_main_color",
            QtCore.QSize(90, 90))

        title = widgets.Label(
            "auth-title",
            "Авторизация",
            gui.main_family.font(17, "Medium"))

        self.login = widgets.LineEdit("auth-login-input", "Логин")
        self.login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password = widgets.PasswordInput("auth-password-input")
        self.password.input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addItem(shorts.VSpacer())
        wrapper = QtWidgets.QFrame(self)
        wl = shorts.VLayout(wrapper)
        wl.addWidget(self.login)
        wl.addWidget(self.password)
        wl.setSpacing(GAP*2)
        layout.addWidget(wrapper)

        # self.accept = custom.getColorButton("arrow-right-circle", "green")
        layout.addItem(shorts.VSpacer())
        # layout.addWidget(self.accept, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.inputs = (self.password, self.login)
        # self.accept.clicked.connect(lambda e: self.signals.send.emit(self.collect()))


class OpenSuggestion(Form):

    """
    Table placeholder with "open" suggestion /
    Виджет, заменяющий таблицу с предложением открыть новый файл или проект
    """

    def __init__(self, window):
        Form.__init__(self, "open suggestion")

        layout = shorts.GLayout(self)

        self.file = widgets.TextButton("document", "Открыть файл", "file-file")
        self.file.clicked.connect(lambda e: window._on_toolbar_button_click("file-file"))
        self.file.clicked.connect(lambda e: self.signals.send.emit({}))
        self.file.label.add_hotkey("Ctrl")
        self.file.label.add_hotkey("O")

        self.folder = widgets.TextButton("folder", "Открыть проект", "file-folder")
        self.folder.clicked.connect(lambda e: window._on_toolbar_button_click("file-folder"))
        self.folder.clicked.connect(lambda e: self.signals.send.emit({}))
        self.folder.label.add_hotkey("Ctrl")
        self.folder.label.add_hotkey("Shift")
        self.folder.label.add_hotkey("O")

        self.cloud = widgets.TextButton("cloud-upload", "Последний", "file-cloud")
        self.cloud.clicked.connect(lambda e: window._on_toolbar_button_click("file-cloud"))
        self.cloud.clicked.connect(lambda e: self.signals.send.emit({}))
        self.cloud.set_shortcut("Ctrl+Alt+O", window)

        wrapper = QtWidgets.QFrame()
        wrapper.setFixedWidth(300)
        wl = shorts.VLayout(wrapper)
        wl.setSpacing(GAP)
        wl.addWidget(self.file)
        wl.addWidget(self.folder)
        wl.addWidget(self.cloud)

        layout.addItem(shorts.VSpacer(), 0, 1, 1, 1)
        layout.addItem(shorts.HSpacer(), 1, 0, 1, 1)
        layout.addItem(shorts.HSpacer(), 1, 2, 1, 1)
        layout.addWidget(wrapper, 1, 1, 1, 1)
        layout.addItem(shorts.VSpacer(), 2, 1, 1, 1)


class MainForm(Form):

    table: tables.Table
    nav: tables.TableNav

    def __init__(self):
        Form.__init__(self, "main form")
        layout = shorts.VLayout(self)
        self.table = tables.Table()
        self.nav = tables.TableNav()
        layout.addWidget(self.nav)
        layout.addWidget(self.table)
        layout.setContentsMargins(GAP, GAP*2, GAP, GAP)
        layout.setSpacing(GAP)
