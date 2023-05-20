from typing import Literal

from PyQt6 import QtWidgets, QtCore, QtGui

from . import config as cfg
from . import shorts
from . import gui
from . import dynamic
from .dynamic import global_widget_manager as gwm


class SvgButton(dynamic.DynamicButton):

    labels: dict[dynamic.widget_trigger, dynamic.DynamicSvg]
    label: dynamic.widget_trigger

    def __init__(
            self,
            labels: dict[dynamic.widget_trigger, dynamic.DynamicSvg]):

        if "leave" not in labels:
            raise ValueError("labels must have 'leave' key!")
        else:
            self.label = "leave"

        dynamic.DynamicButton.__init__(self)
        self.labels = labels
        self.signals.triggered.connect(lambda trigger: self.show_label(trigger))
        self.setFixedSize(cfg.BUTTONS_SIZE)

        layout = shorts.GLayout(self)
        for name, label in labels.items():
            layout.addWidget(label, 0, 0, 1, 1)
            if name != "leave":
                label.hide()

    def show_label(self, trigger: dynamic.widget_trigger):
        if trigger in self.labels and trigger != self.label:
            self.labels[self.label].hide()
            self.label = trigger
            self.labels[trigger].show()


def get_regular_button(
        object_name: str,
        icon_name: str) -> SvgButton:

    icon = dynamic.DynamicSvg(icon_name, "main")
    button = SvgButton({"leave": icon})
    gwm.add_widget(button, object_name, "button")
    return button


def get_color_button(
        object_name: str,
        icon_name: str,
        color_name: dynamic.color_name):

    leave_icon = dynamic.DynamicSvg(icon_name, "main")
    hover_icon = dynamic.DynamicSvg(icon_name, "alter")

    button = SvgButton({
        "leave": leave_icon,
        "hover": hover_icon
    })

    gwm.add_widget(button, object_name)
    object_name = button.objectName()
    gwm.set_style(object_name, "always", dynamic.always % cfg.radius())
    gwm.set_style(object_name, "leave", "background-color: !back!")
    gwm.set_style(object_name, "hover", f"background-color: !{color_name}!")

    return button


class Label(dynamic.DynamicLabel):

    """
    Simple label widget /
    Простой виджет метки
    """

    def __init__(
            self,
            text: str,
            font: gui.Font):

        dynamic.DynamicLabel.__init__(self)
        self.setWordWrap(True)
        self.setText(text)
        self.setFont(font)


class HotkeyHint(Label):

    """
    small label that shows the hotkey /
    небольшая метка, отображающая горячую клавишу
    """

    def __init__(self, key: str):
        Label.__init__(
            self,
            key,
            gui.main_family.font(size=10, style="Medium")
        )

        self.setFixedHeight(int(cfg.BUTTONS_SIZE.height()/2))
        self.setSizePolicy(shorts.MinimumPolicy())
        self.setContentsMargins(1, 1, 1, 1)


class ButtonLabel(dynamic.DynamicFrame):

    """
    label with hotkey hints /
    метка с подсказкой горячей клавиши
    """

    def __init__(self, text: str):

        dynamic.DynamicFrame.__init__(self)
        layout = shorts.HLayout(self)
        layout.setSpacing(cfg.GAP)
        self.keys = QtWidgets.QFrame()
        klayout = shorts.HLayout(self.keys)
        klayout.setSpacing(2)
        self.label = Label(text, gui.main_family.font())
        self.label.setWordWrap(False)
        layout.addWidget(self.label)
        layout.addItem(shorts.HSpacer())
        layout.addWidget(self.keys)

    def setText(self, text: str):
        return self.label.setText(text)

    def text(self):
        return self.label.text()

    def add_hotkey(self, key: str):
        hint = HotkeyHint(key)
        hint.dont_translate = True
        self.keys.layout().addWidget(hint)
        gwm.add_widget(hint)
        gwm.set_style(
            hint,
            "always",
            "border-radius: 4px; outline: none;")
        gwm.set_style(
            hint,
            "leave",
            "color: !highlight1!; border: 1px solid !highlight1!;"
        )


class TextButton(dynamic.DynamicButton):

    def __init__(self, text: str, font: gui.Font = None):
        dynamic.DynamicButton.__init__(self)
        self.setText(text)
        font = font if font else gui.main_family.font()
        self.setFont(font)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())


class SvgTextButton(dynamic.DynamicButton):

    """
    Regular button with text and icon /
    Стандартная кнопка с текстом и иконкой
    """

    def __init__(
            self,
            icon_name: str,
            text: str):

        dynamic.DynamicButton.__init__(self)

        self.icon_ = dynamic.DynamicSvg(
            icon_name,
            "main",
            cfg.BUTTONS_SIZE
        )
        self.label = ButtonLabel(text)

        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        layout = shorts.HLayout(self)
        layout.addWidget(self.icon_)
        layout.addWidget(self.label)
        layout.setSpacing(2)
        layout.addItem(shorts.HSpacer())

    def setText(self, text: str) -> None:
        return self.label.setText(text)

    def text(self) -> str:
        return self.label.text()

    def setStyleSheet(self, styleSheet: str) -> None:
        self.label.setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)

    def set_shortcut(self, hotkey: str):
        for key in hotkey.split("+"):
            self.label.add_hotkey(key)


class LineEdit(dynamic.DynamicLineEdit):

    """
    Simple line input widget /
    Простой виджет ввода строки
    """

    def __init__(
            self,
            placeholder: str):

        dynamic.DynamicLineEdit.__init__(self)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setFont(gui.main_family.font())


class SwitchingButton(dynamic.DynamicButton):

    """
    Button switching it's icon by click /
    Кнопка, переключающая свою иконку по клику
    """

    icons: tuple[str, dynamic.DynamicSvg]
    icon: tuple[str, dynamic.DynamicSvg]

    def __init__(
            self,
            *icons: tuple[str, dynamic.DynamicSvg]):

        dynamic.DynamicButton.__init__(self)
        self.icons = icons
        self.setFixedSize(cfg.BUTTONS_SIZE)
        layout = shorts.GLayout(self)
        for i, icon in enumerate(icons):
            layout.addWidget(icon[1], 0, 0, 1, 1)
            if i != 0:
                icon[1].hide()
            else:
                self.icon = icon
        self.clicked.connect(lambda e: self.switch())

    def switch(self):
        message = self.icon[0]
        for i, icon in enumerate(self.icons):
            if icon[1] == self.icon[1]:
                self.icon[1].hide()
                break
        self.icon = self.icons[i+1 if i+1 < len(self.icons) else 0]
        self.icon[1].show()
        self.signals.triggered.emit(message)


class PasswordInput(dynamic.DynamicFrame):

    """
    LineEdit with switching text visility /
    LineEdit с переключаемой видимостью текста
    """

    def __init__(self):

        dynamic.DynamicFrame.__init__(self)
        self.input = LineEdit("Пароль")

        layout = shorts.GLayout(self)
        show = dynamic.DynamicSvg("eye", "main")
        hide = dynamic.DynamicSvg("eye-slash", "main")

        self.eye = SwitchingButton(("show", show), ("hide", hide))
        self.eye.signals.triggered.connect(
            lambda trigger: self.show_password(trigger))

        self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(self.input, 0, 0, 1, 1)
        layout.addWidget(self.eye, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)

    def setPlaceholderText(self, text: str) -> str:
        return self.input.setPlaceholderText(text)

    def placeholderText(self) -> str:
        return self.input.placeholderText()

    def show_password(self, trigger: str):
        if trigger == "show":
            self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        elif trigger == "hide":
            self.input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


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


class RadioButton(dynamic.DynamicFrame):

    button0: QtWidgets.QPushButton
    button1: QtWidgets.QPushButton
    active: bool = False

    def __init__(
            self,
            button0: QtWidgets.QPushButton,
            button1: QtWidgets.QPushButton):

        dynamic.DynamicFrame.__init__(self)
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
        pass

    def switch(self, active: bool):
        if active:
            self.button0.hide()
            self.button1.show()
        else:
            self.button1.hide()
            self.button0.show()
        self.active = active


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
