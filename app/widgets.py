from PyQt6 import QtWidgets, QtCore

from . import custom_widgets as custom
from . import config as cfg
from .config import GAP
from . import events
from . import shorts
from . import gui
from .personalization import personalization


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


class AbstractLabel(QtWidgets.QLabel):

    """
    Simple label widget /
    Простой виджет метки
    """

    def __init__(self, text: str, font: gui.Font):
        QtWidgets.QLabel.__init__(self)
        self.setWordWrap(True)
        self.setText(text)
        self.setFont(font)


@decorator
class Label(AbstractLabel):
    pass


class AbstractHotkeyHint(AbstractLabel):

    """
    small label that shows the hotkey /
    небольшая метка, отображающая горячую клавишу
    """

    def __init__(self, key: str):
        AbstractLabel.__init__(self, key, gui.main_family.font(size=10, style="Medium", weight=600))
        self.setFixedHeight(16)
        self.setSizePolicy(shorts.MinimumPolicy())
        self.setContentsMargins(4, 2, 4, 2)


@personalization(
    (
        """
        outline: none;
        border: none;
        border-radius: 4px;
        """,
        {
            "color": "back",
            "background-color": "hotkeys"
        }
    )
)
class HotkeyHint(AbstractHotkeyHint):
    pass


class ButtonLabel(QtWidgets.QFrame):

    """
    label with hotkey hints /
    метка с подсказкой горячей клавиши
    """

    def __init__(self, text: str):
        QtWidgets.QFrame.__init__(self)
        layout = shorts.HLayout(self)
        layout.setSpacing(12)
        self.keys = QtWidgets.QFrame()
        klayout = shorts.HLayout(self.keys)
        klayout.setSpacing(4)
        self.label = Label(text, gui.main_family.font())
        layout.addWidget(self.label)
        layout.addWidget(self.keys)

    def setText(self, text: str):
        return self.label.setText(text)

    def text(self):
        return self.label.text()

    def add_hotkey(self, key: str):
        hint = HotkeyHint(key)
        self.keys.layout().addWidget(hint)


class AbstractTextButton(events.HoverableButton):

    """
    Regular button with text and icon /
    Стандартная кнопка с текстом и иконкой
    """

    def __init__(self, icon_name: str, text: str, object_name: str):

        events.HoverableButton.__init__(self)

        self.icon_ = custom.SvgLabel(icon_name, "icons_main_color", cfg.BUTTONS_SIZE)
        self.label = ButtonLabel(text)

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

    def set_shortcut(self, hotkey: str, window: QtWidgets.QMainWindow):
        keys = hotkey.split("+")
        for key in keys:
            self.label.add_hotkey(key)
        return super().set_shortcut(hotkey, window)


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
class TextButton(AbstractTextButton):
    pass


class AbstractLineEdit(QtWidgets.QLineEdit):

    """
    Simple line input widget /
    Простой виджет ввода строки
    """

    def __init__(self, placeholder: str):
        QtWidgets.QLineEdit.__init__(self)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setFont(gui.main_family.font())


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
class LineEdit(AbstractLineEdit):
    pass


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


class ScrollArea(QtWidgets.QScrollArea):

    """
    Vertical scroll area with hidden srollbars /
    Вертикальная область прокрутки без видимых полос прокрутки
    """

    def __init__(self):
        QtWidgets.QScrollArea.__init__(self)
        self.setSizePolicy(shorts.ExpandingPolicy())
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().setEnabled(True)
        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.area = QtWidgets.QFrame()
        layout = shorts.VLayout(self.area)
        layout.setSpacing(40)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setWidget(self.area)
