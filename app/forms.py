from PyQt6 import QtWidgets, QtCore

from . import widgets
from . import shorts
from .config import GAP
from . import config as cfg
from . import gui
from . import tables
from . import dynamic
from .dynamic import global_widget_manager as gwm


class Form(dynamic.DynamicFrame):

    """
    Simple frame that can emit "send" signal
    and collect inputed data to a dictionary /
    Простой фрейм, который может испускать сигнал "send"
    и собирать собранные данные в словарь
    """

    inputs: tuple[QtWidgets.QWidget]

    def __init__(self):
        dynamic.DynamicFrame.__init__(self)

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
        Form.__init__(self)
        self.setFixedSize(250, 300)

        layout = shorts.VLayout(self)

        icon = dynamic.DynamicSvg("circle-person", "main", cfg.ICONS_LARGE_SIZE)
        title = widgets.Label("Авторизация", gui.main_family.font(17, "Medium"))
        gwm.add_widget(title, "auth-title", "label")

        self.login = widgets.LineEdit("Логин")
        gwm.add_widget(self.login, "auth-login", "input")
        self.login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password = widgets.PasswordInput()
        gwm.add_widget(self.password, "auth-password", "input")
        self.password.input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addItem(shorts.VSpacer())
        wrapper = QtWidgets.QFrame(self)
        wl = shorts.VLayout(wrapper)
        wl.addWidget(self.login)
        wl.addWidget(self.password)
        wl.setSpacing(GAP)
        layout.addWidget(wrapper)

        self.accept = widgets.get_color_button("auth-accept", "arrow-right-circle", "green")
        gwm.add_shortcut(self.accept.click, "Enter")
        layout.addItem(shorts.VSpacer())
        layout.addWidget(self.accept, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.inputs = (self.password, self.login)
        self.accept.clicked.connect(lambda e: self.signals.triggered.emit("log in"))


class OpenSuggestion(Form):

    """
    Table placeholder with "open" suggestion /
    Виджет, заменяющий таблицу с предложением открыть новый файл или проект
    """

    def __init__(self):
        Form.__init__(self)

        layout = shorts.GLayout(self)

        self.file = widgets.SvgTextButton("document", "Открыть файл")
        gwm.add_widget(self.file, "open-file", "button")
        self.file.label.add_hotkey("Ctrl")
        self.file.label.add_hotkey("O")

        self.folder = widgets.SvgTextButton("folder", "Открыть папку")
        gwm.add_widget(self.folder, "open-folder", "button")
        self.folder.label.add_hotkey("Ctrl")
        self.folder.label.add_hotkey("Shift")
        self.folder.label.add_hotkey("O")

        self.cloud = widgets.SvgTextButton("cloud-upload", "Открыть последний")
        gwm.add_widget(self.cloud, "open-last", "button")
        self.cloud.set_shortcut("Ctrl+Alt+O")
        gwm.add_shortcut(self.cloud.click, "Ctrl+Alt+O")

        wrapper = dynamic.DynamicFrame()
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
        Form.__init__(self)
        layout = shorts.VLayout(self)
        self.table = tables.Table()
        self.nav = tables.TableNav()
        layout.addWidget(self.nav)
        layout.addWidget(self.table)
        layout.setContentsMargins(GAP, GAP*2, GAP, GAP)
        layout.setSpacing(GAP)
