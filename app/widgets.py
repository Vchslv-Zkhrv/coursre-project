from typing import Literal

from PyQt6 import QtWidgets, QtCore, QtSvg, QtGui

from . import config as cfg
from . import shorts
from . import gui
from . import dynamic


class SvgLabel(dynamic.DynamicLabel):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(
            self,
            object_name: str,
            icon_name: str,
            icon_color_name: Literal["icons_main_color", "icons_alter_color"] = "icons_main_color",
            size: QtCore.QSize = None):

        dynamic.DynamicLabel.__init__(self, object_name)
        self.icon_name = icon_name
        size = size if size else cfg.ICONS_SIZE
        self.setFixedSize(size)
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_icon()
        self.setStyleSheet(
            f"border-radius: {cfg.radius()}px; background-color: none;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def update_icon(self):
        renderer = QtSvg.QSvgRenderer(
            cfg.icon("black", self.icon_name))
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setPixmap(pixmap)


class SvgButton(dynamic.DynamicButton):

    """
    QPushButton with svg icon with to states: normal and hovered /
    Виджет QPushButton с svg - иконкой и двумя состояниями: обьчное и наведенное
    """

    def __init__(
            self,
            object_name: str,
            label0: SvgLabel,
            label1: SvgLabel):

        dynamic.DynamicButton.__init__(self, object_name)

        # все кнопки имеют единый стиль
        self.setFixedSize(cfg.BUTTONS_SIZE)
        # макет
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # обе иконки помещаются на макет и скрываются
        layout.addWidget(label0)
        layout.addWidget(label1)
        label0.hide()
        label1.hide()
        self.label0 = label0
        self.label1 = label1


class Label(dynamic.DynamicLabel):

    """
    Simple label widget /
    Простой виджет метки
    """

    def __init__(
            self,
            object_name: str,
            text: str,
            font: gui.Font):

        dynamic.DynamicLabel.__init__(self, object_name)
        self.setWordWrap(True)
        self.setText(text)
        self.setFont(font)


class HotkeyHint(Label):

    """
    small label that shows the hotkey /
    небольшая метка, отображающая горячую клавишу
    """

    def __init__(self, object_name: str, key: str):
        Label.__init__(
            self,
            object_name,
            key,
            gui.main_family.font(size=10, style="Medium", weight=600)
        )

        self.setFixedHeight(16)
        self.setSizePolicy(shorts.MinimumPolicy())
        self.setContentsMargins(4, 2, 4, 2)


class ButtonLabel(dynamic.DynamicLabel):

    """
    label with hotkey hints /
    метка с подсказкой горячей клавиши
    """

    def __init__(
            self,
            object_name: str,
            text: str):

        QtWidgets.QFrame.__init__(self, object_name)
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
        hint = HotkeyHint(f"{self.objectName()} {key} hint", key)
        self.keys.layout().addWidget(hint)


class TextButton(dynamic.DynamicButton):

    """
    Regular button with text and icon /
    Стандартная кнопка с текстом и иконкой
    """

    def __init__(
            self,
            object_name: str,
            icon_name: str,
            text: str):

        dynamic.DynamicButton.__init__(self, object_name)

        self.icon_ = SvgLabel(
            f"{object_name}-icon",
            icon_name,
            "icons_main_color",
            cfg.BUTTONS_SIZE
        )
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

    def set_shortcut(self, hotkey: str):
        keys = hotkey.split("+")
        for key in keys:
            self.label.add_hotkey(key)


class LineEdit(dynamic.DynamicLineEdit):

    """
    Simple line input widget /
    Простой виджет ввода строки
    """

    def __init__(
            self,
            object_name: str,
            placeholder: str):

        dynamic.DynamicLineEdit.__init__(self, object_name)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.setFont(gui.main_family.font())


class SwitchingButton(dynamic.DynamicFrame):

    """
    Button switching it's icon by click /
    Кнопка, переключающая свою иконку по клику
    """

    icons: tuple[SvgButton]

    def __init__(
            self,
            object_name: str,
            *states: tuple[str, str]):

        dynamic.DynamicFrame.__init__(self, object_name)
        self.setFixedSize(cfg.BUTTONS_SIZE)
        layout = shorts.GLayout(self)


class PasswordInput(dynamic.DynamicFrame):

    """
    LineEdit with switching text visility /
    LineEdit с переключаемой видимостью текста
    """

    def __init__(
            self,
            object_name: str):

        dynamic.DynamicFrame.__init__(self, object_name)
        self.input = LineEdit(f"{object_name}-line", "Пароль")

        layout = shorts.GLayout(self)
        self.eye = SwitchingButton(
            f"{object_name}-eye",
            ("eye", "show password"),
            ("eye-slash", "hide password")
        )

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
            object_name: str,
            window,
            icon_name: str,
            text: str,
            width: int):

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


class RadioButton(dynamic.DynamicFrame):

    button0: QtWidgets.QPushButton
    button1: QtWidgets.QPushButton
    active: bool = False

    def __init__(
            self,
            object_name: str,
            button0: QtWidgets.QPushButton,
            button1: QtWidgets.QPushButton):

        dynamic.DynamicFrame.__init__(self, object_name)
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
