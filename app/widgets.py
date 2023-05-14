from PyQt6 import QtWidgets, QtCore

from . import custom_widgets as custom
from . import config as cfg
from .config import GAP
from . import events
from . import shorts
from . import gui
from .personalization import personalization
from .personalization import rgba, CURRENT_THEME as THEME

"""
Module with final widgets classes / Модуль с классами конечных виджетов.

The classes in this module should be treated as singletons,
but PyQt6 does not allow this pattern /
Классы в этом модуле стоит воспринимать как синглтоны,
однако библиотека PyQt6 не позволяет безопасно применять этот паттерн

"""

decorator = personalization((
    "border: none; outline: none; background-color: none;",
    {"color": "fore"}
))


@decorator
class Button(QtWidgets.QPushButton):
    pass


@decorator
class Frame(QtWidgets.QFrame):
    pass


@decorator
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


@personalization(
    (
        f"""
            border: none;
            border-radius: {cfg.radius()}px;
            outline: none;
        """,
        {
            "color": "fore",
            "background-color": "back"
        }
    ),
    (
        f"""
            border: none;
            border-radius: {cfg.radius()}px;
            outline: none;
        """,
        {
            "color": "fore",
            "background-color": "highlight1"
        }
    )
)
class TextButton(events.HoverableButton):

    """
    Regular button with text and icon /
    Стандартная кнопка с текстом и иконкой
    """

    def __init__(self, icon_name: str, text: str, object_name: str):

        events.HoverableButton.__init__(self)

        self.icon_ = custom.SvgLabel(icon_name, "icons_main_color", cfg.BUTTONS_SIZE)
        self.label = Label(text, gui.main_family.font())

        self.setObjectName(object_name)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        layout = shorts.HLayout(self)
        layout.addWidget(self.icon_)
        layout.addWidget(self.label)
        layout.setSpacing(2)
        layout.addItem(shorts.HSpacer())

    def setStyleSheet(self, styleSheet: str) -> None:
        self.label.setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)


@personalization((
    f"""
        outline: none;
        border: none;
        border-radius: {cfg.radius()}px;
        padding-right: {GAP}px;
        padding-left: {GAP}px;
    """,
    {
        "background-color": "highlight2",
        "color": "fore"
     }
))
class LineEdit(QtWidgets.QLineEdit):

    """
    Simple line input widget /
    Простой виджет ввода строки
    """

    def __init__(self, placeholder: str):
        QtWidgets.QLineEdit.__init__(self)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setFont(gui.main_family.font())


class SwitchingButton(QtWidgets.QFrame):

    """
    Button switching it's icon by click /
    Кнопка, переключающая свою иконку по клику
    """

    icons: tuple[custom.SvgButton]

    def __init__(self, *states: tuple[str, str]):
        QtWidgets.QFrame.__init__(self)
        self.signals = events.SwitchingButtonSignals()
        self.setFixedSize(cfg.BUTTONS_SIZE)
        self.setStyleSheet("""
            outline: none;
            background-color: none;
            color: none;
            border: none""")
        layout = shorts.GLayout(self)

        self.icons = tuple(custom.getRegularButton(state[0]) for state in states)
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
        self.eye.signals.switched.connect(self.hide_password)
        for b in self.eye.icons:
            b.signals.hovered.emit()
            b.signals.blockSignals(True)

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

    def __init__(
            self,
            window,
            icon_name: str,
            text: str,
            width: int,
            object_name: str):

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
