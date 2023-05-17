from typing import Literal

from PyQt6 import QtWidgets, QtCore

from . import custom_widgets as custom
from . import config as cfg
from . import events
from . import shorts
from . import gui


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


class HotkeyHint(Label):

    """
    small label that shows the hotkey /
    небольшая метка, отображающая горячую клавишу
    """

    def __init__(self, key: str):
        Label.__init__(self, key, gui.main_family.font(size=10, style="Medium", weight=600))
        self.setFixedHeight(16)
        self.setSizePolicy(shorts.MinimumPolicy())
        self.setContentsMargins(4, 2, 4, 2)


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


class TextButton(events.HoverableButton):

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

    def text(self) -> str:
        return self.label.text()

    def setStyleSheet(self, styleSheet: str) -> None:
        self.label.setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)

    def set_shortcut(self, hotkey: str, window: QtWidgets.QMainWindow):
        keys = hotkey.split("+")
        for key in keys:
            self.label.add_hotkey(key)
        return super().set_shortcut(hotkey, window)


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

        self.icons = tuple(events.HoverableButton() for state in states)
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


class VScrollArea(QtWidgets.QScrollArea):

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
        self.setWidget(self.area)


class HScrollArea(QtWidgets.QScrollArea):

    """
    Horizontal scroll area with hidden srollbars /
    Горизонтальная область прокрутки без видимых полос прокрутки
    """

    def __init__(self):
        QtWidgets.QScrollArea.__init__(self)
        self.setSizePolicy(shorts.ExpandingPolicy())
        self.setWidgetResizable(True)
        self.verticalScrollBar().setDisabled(True)
        self.horizontalScrollBar().setEnabled(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.area = QtWidgets.QFrame()
        self.setWidget(self.area)


class ScrollArea(QtWidgets.QScrollArea):

    """
    Both-dimensional scroll area with hidden srollbars /
    Горизонтальная и вертикальная область прокрутки без видимых полос прокрутки
    """

    def __init__(self):
        QtWidgets.QScrollArea.__init__(self)
        self.setSizePolicy(shorts.ExpandingPolicy())
        self.setWidgetResizable(True)
        self.verticalScrollBar().setEnabled(True)
        self.horizontalScrollBar().setEnabled(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.area = QtWidgets.QFrame()
        self.setWidget(self.area)


class RadioButton(QtWidgets.QFrame):

    button0: QtWidgets.QPushButton
    button1: QtWidgets.QPushButton
    active: bool = False

    def __init__(
            self,
            button0: QtWidgets.QPushButton,
            button1: QtWidgets.QPushButton):

        QtWidgets.QFrame.__init__(self)
        self.signals = events.RadioButtonSignals()
        self.button0 = button0
        self.button1 = button1

        layout = shorts.GLayout(self)
        layout.addWidget(button0)
        layout.addWidget(button1)
        self.switch(False)

        button0.clicked.connect(lambda e: self.ask_to_switch(True))
        button1.clicked.connect(lambda e: self.ask_to_switch(False))

    def text(self) -> str:
        if self.active:
            return self.button1.text()
        else:
            return self.button0.text()

    def ask_to_switch(self, active: bool):
        self.signals.clicked.emit(active)

    def switch(self, active: bool):
        if active:
            self.button0.hide()
            self.button1.show()
        else:
            self.button1.hide()
            self.button0.show()
        self.active = active


def getRadioSvgButton(text: str) -> RadioButton:
    b0 = TextButton("circle-small", text, f"{text}-off")
    b1 = TextButton("circle-filled-small", text, f"{text}-on")
    return RadioButton(b0, b1)


def getCheckSvgButton(text: str) -> RadioButton:
    b0 = TextButton("square-small", text, f"{text}-off")
    b1 = TextButton("square-small-filled", text, f"{text}-on")
    return RadioButton(b0, b1)




class RadioGroup(ScrollArea):

    radios: list[RadioButton] = []
    one_only: bool

    def __init__(
            self,
            direction: Literal["v", "h"],
            one_only: bool,
            *radios: RadioButton):
        ScrollArea.__init__(self)

        self.one_only = one_only
        self.radio_signals = events.RadioGroupSignals()
        if direction == "v":
            layout = shorts.VLayout(self.area)
            spacer = shorts.VSpacer()
            layout.setDirection(QtWidgets.QVBoxLayout.Direction.BottomToTop)
        else:
            layout = shorts.HLayout(self.area)
            spacer = shorts.HSpacer()
            layout.setDirection(QtWidgets.QVBoxLayout.Direction.RightToLeft)
        layout.addItem(spacer)
        self.add_radios(*radios)

    def drop_radios(self):
        for radio in self.radios:
            radio.hide()
        self.radios = []

    def add_radios(self, *radios: RadioButton):
        indent = len(self.radios)
        self.radios.extend(radios)
        for i, radio in enumerate(radios):
            self.area.layout().addWidget(radio)
            radio.signals.clicked.connect(
                lambda active, index=i+indent:
                self._on_radio_click(active, index))
        if radios:
            radios[-1].button0.click()
            radios[-1].switch(True)

    def _click_radio(self, index: int):
        current_index = 0
        for i, r in enumerate(self.radios):
            if r.active:
                current_index = i
        if index == current_index:
            return
        else:
            self.radios[current_index].switch(False)
            self.radios[index].switch(True)

    def _click_checkbox(self, active: bool, index: int):
        self.radios[index].switch(active)

    def _on_radio_click(self, active: bool, index: int):
        if self.one_only:
            self._click_radio(index)
        else:
            self._click_radio(active, index)
        self.radio_signals.radio_click.emit(index)

    def get_choosen_radios(self) -> tuple[RadioButton]:
        radios = []
        for radio in self.radios:
            if radio.active:
                radios.append(radio)
        return tuple(radios)
