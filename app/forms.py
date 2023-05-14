from PyQt6 import QtWidgets, QtCore

from .events import FormSignals
from . import widgets
from . import shorts
from . import custom_widgets as custom
from .config import GAP
from . import gui


class Form(widgets.Frame):

    """
    Simple frame that can emit "send" signal
    and collect inputed data to a dictionary /
    Простой фрейм, который может испускать сигнал "send"
    и собирать собранные данные в словарь
    """

    inputs: tuple[QtWidgets.QWidget]

    def __init__(self):
        widgets.Frame.__init__(self)
        self.signals = FormSignals()

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
        self.setStyleSheet("""
            border: none;
            color: none;
            background-color: none""")
        self.setFixedSize(250, 300)

        layout = shorts.VLayout(self)
        icon = custom.SvgLabel(
            "circle-person",
            "icons_main_color",
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
        wl.setSpacing(GAP*2)
        layout.addWidget(wrapper)

        self.accept = custom.getColorButton("arrow-right-circle", "green")
        layout.addItem(shorts.VSpacer())
        layout.addWidget(self.accept, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.inputs = (self.password, self.login)
        self.accept.clicked.connect(lambda e: self.signals.send.emit(self.collect()))


class OpenSuggestion(Form):

    """
    Table placeholder with "open" suggestion /
    Виджет, заменяющий таблицу с предложением открыть новый файл или проект
    """

    def __init__(self, window):
        Form.__init__(self)

        layout = shorts.GLayout(self)

        self.file = widgets.TextButton("document", "Открыть файл", "file-file")
        self.file.clicked.connect(lambda e: window._on_toolbar_button_click("file-file"))
        self.file.clicked.connect(lambda e: self.signals.send.emit({}))

        self.folder = widgets.TextButton("folder", "Открыть проект", "file-folder")
        self.folder.clicked.connect(lambda e: window._on_toolbar_button_click("file-folder"))
        self.folder.clicked.connect(lambda e: self.signals.send.emit({}))

        self.cloud = widgets.TextButton("cloud-upload", "Последний", "file-cloud")
        self.cloud.clicked.connect(lambda e: window._on_toolbar_button_click("file-cloud"))
        self.cloud.clicked.connect(lambda e: self.signals.send.emit({}))
        self.cloud.set_shortcut("Ctrl+Alt+O", window)

        wrapper = QtWidgets.QFrame()
        wrapper.setFixedWidth(200)
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
    pass
