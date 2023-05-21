from dataclasses import dataclass
from typing import Literal, TypedDict, Callable
import locale
import json
import os

from PyQt6 import QtWidgets, QtGui, QtCore, QtSvg
from .cwindow import CWindow
import keyboard
from loguru import logger

from . import config as cfg
from . import shorts


system_lang = locale.getdefaultlocale()[0][:2]


class Vocabulary(TypedDict):

    languages: tuple[str]
    translations: tuple[tuple[str]]


def get_vocabulary() -> Vocabulary:
    with open(f"{os.getcwd()}\\{cfg.VOCABULARY_PATH}", encoding="utf-8") as source:
        return json.load(source)


def rgba(color: QtGui.QColor):
    r, g, b, a = color.getRgb()
    return f"rgba({r}, {g}, {b}, {a})"


color_name = Literal[
    "dim",
    "fore",
    "back",
    "highlight1",
    "highlight2",
    "red",
    "yellow",
    "green",
    "blue",
    "hotkeys"
]


class Theme(TypedDict):
    theme_icon: str
    dim: QtGui.QColor
    fore: QtGui.QColor
    back: QtGui.QColor
    highlight1: QtGui.QColor
    highlight2: QtGui.QColor
    hotkeys: QtGui.QColor
    red: QtGui.QColor
    yellow: QtGui.QColor
    green: QtGui.QColor
    blue: QtGui.QColor
    icons_main_color: str
    icons_alter_color: str


def parse_config_themes() -> dict[str, Theme]:
    themes = {}
    for name, colors in cfg.THEMES.items():
        colors_ = {}
        for key, value in colors.items():
            if isinstance(value, tuple) and key != "theme_icon":
                colors_[key] = QtGui.QColor(*value)
            else:
                colors_[key] = value
        themes[name] = colors_
    return themes


widget_trigger = Literal[
    "always",
    "hover",
    "leave",
    "active",
    "active_hover",
    "hotkey",
    "click"
]

widget_type = Literal[
    "window",
    "frame",
    "input",
    "popup_sea",
    "popup_island",
    "button",
    "frame",
    "label"
]


class DynamicWidgetSignals(QtCore.QObject):

    triggered = QtCore.pyqtSignal(str)


class GlobalSignals(QtCore.QObject):

    switch_theme = QtCore.pyqtSignal(str)
    switch_lang = QtCore.pyqtSignal(str)
    switch_scale = QtCore.pyqtSignal(float)


class DynamicWidget(QtWidgets.QWidget):

    """
    widget that can be used in Global class /
    Виджет, который может быть использован в классе Global
    """

    signals: DynamicWidgetSignals

    styles: dict[widget_trigger, str]
    state: widget_trigger
    dont_translate: bool

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.signals = DynamicWidgetSignals()
        self.styles = {}
        self.state = "leave"
        self.dont_translate = False


class DynamicLabel(QtWidgets.QLabel, DynamicWidget):
    pass


class DynamicSvg(QtWidgets.QLabel, DynamicWidget):

    icon_color: Literal["main", "alter"]
    icon_name: str

    def __init__(
            self,
            icon_name: str,
            icon_color: Literal["main", "alter"],
            size: QtCore.QSize = cfg.ICONS_SIZE):

        DynamicWidget.__init__(self)
        QtWidgets.QLabel.__init__(self)
        assert icon_color in ("main", "alter")
        self.icon_name = icon_name
        self.icon_color = icon_color
        self.setFixedSize(size)
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            f"border-radius: {cfg.radius()}px; background-color: none;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        global_widget_manager.add_widget(self)

    def draw_icon(self, icon_color: str):
        renderer = QtSvg.QSvgRenderer(
            cfg.icon(icon_color, self.icon_name))
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setPixmap(pixmap)


class DynamicButton(QtWidgets.QPushButton, DynamicWidget):

    def __init__(self):
        self.hovered = False
        DynamicWidget.__init__(self)
        QtWidgets.QPushButton.__init__(self)
        self.clicked.connect(lambda e: self.signals.triggered.emit("click"))

    def _set_hovered(self, hovered: bool):
        if hovered:
            self.signals.triggered.emit("hover")
        else:
            self.signals.triggered.emit("leave")

    def event(self, e: QtCore.QEvent) -> bool:
        if isinstance(e, QtGui.QHoverEvent):
            if e.position().x() < 0:
                hover = False
            else:
                hover = True
            if hover != self.hovered:
                if hover:
                    self._set_hovered(True)
                else:
                    self._set_hovered(False)
                self.hovered = hover
        return super().event(e)


class DynamicLineEdit(QtWidgets.QLineEdit, DynamicWidget):
    pass


class DynamicFrame(QtWidgets.QFrame, DynamicWidget):
    pass


class DynamicScrollArea(QtWidgets.QScrollArea, DynamicWidget):
    pass


class DynamicWindow(CWindow, DynamicWidget):

    def __init__(self):
        DynamicWidget.__init__(self)
        CWindow.__init__(self)

    def blur(self, blur: bool):
        effect = QtWidgets.QGraphicsBlurEffect()
        if blur:
            effect.setBlurRadius(3)
        else:
            effect.setBlurRadius(0)
        self.setGraphicsEffect(effect)


class DynamicDialog(QtWidgets.QDialog, DynamicWidget):
    pass


class NonUniqueObjectNameError(Exception):
    pass


@dataclass
class GlobalHook():

    callback: Callable
    trigger: widget_trigger
    filter_: Callable


class Global():

    """
    Global virtual object that allows widgets managing /
    Глобальный виртуальный объект, который позволяет управлять виджетами
    """

    widgets: dict[str, DynamicWidget]
    themes: dict[str, Theme]
    theme: Theme
    theme_name: str
    window: DynamicWindow = None
    shortcuts: dict[str, DynamicWidget]
    languages: tuple[str]
    language: str
    hooks: list[GlobalHook]
    vocabulary: Vocabulary

    def __init__(self):

        self.last_autogenerated_object_name = 0
        self.signals = GlobalSignals()
        self.themes = parse_config_themes()
        self.widgets = {}
        self.languages = get_vocabulary()["languages"]
        self.language = system_lang
        self.shortcuts = {}
        self.hooks = []

        if "main" in self.themes:
            key = "main"
        elif "light" in self.themes:
            key = "light"
        else:
            key = sorted(tuple(self.themes.keys()))[0]

        self.theme = self.themes[key]
        self.theme_name = key

    def switch_language(self, language: str):
        self.language = language
        self.vocabulary = get_vocabulary()
        for widget in self.widgets.values():
            if widget.dont_translate:
                continue
            if hasattr(widget, "setPlaceholderText") and widget.placeholderText():
                widget.setPlaceholderText(self.translate(widget.placeholderText()))
            elif hasattr(widget, "setText") and widget.text():
                widget.setText(self.translate(widget.text()))
        del self.vocabulary

    def add_widget(
            self,
            widget: DynamicWidget,
            object_name: str = None,
            style_preset: widget_type = None):

        """
        Adds widget to global heap. \
        Добавляет виджет в глобальный набор
        """
        if not object_name:
            self.last_autogenerated_object_name += 1
            object_name = str(self.last_autogenerated_object_name)

        if object_name in self.widgets:
            raise ValueError("widget name repeat")
        if widget in self.widgets.values():
            raise ValueError("widget repeat")

        widget.setObjectName(object_name)

        self.widgets[object_name] = widget
        widget.signals.triggered.connect(
            lambda trigger: self._widget_triggered(widget, trigger))

        if style_preset:
            self.use_preset(object_name, style_preset)

    def _widget_triggered(self, widget: DynamicWidget, trigger: widget_trigger):
        self._check_hooks(widget, trigger)
        if trigger in widget.styles:
            widget.state = trigger
            self.update_style(widget)

    def _check_hooks(self, widget: DynamicWidget, trigger: widget_trigger):

        for hook in self.hooks:

            if hook.trigger == trigger and hook.filter_(widget):
                hook.callback(widget.objectName())

    def add_hook(
            self,
            callback: Callable,
            trigger: widget_trigger,
            filter_: Callable = None):

        """
        Calls callback(widget.objectName()) when trigger occurs
        if filter(widget) returns True
        """
        if not filter_:
            filter_ = lambda widget: True
        self.hooks.append(GlobalHook(callback, trigger, filter_))

    def _generate_widget_style(self, stylesheet: str) -> str:
        if "!" in stylesheet:
            before, substr, *after = stylesheet.split("!")
            before = f"{before}{rgba(self.theme[substr])}"
            after = "!".join(after)
            if "!" in after:
                after = self._generate_widget_style(after)
            return before + after
        else:
            return stylesheet

    def switch_theme(self, name: str):
        self.theme = self.themes[name]
        self.theme_name = name
        for widget in self.widgets.values():
            if isinstance(widget, DynamicSvg) and hasattr(widget, "icon_color"):
                self.update_icon_color(widget)
            else:
                self.update_style(widget)

    def update_icon_color(self, icon: DynamicSvg):
        icon.draw_icon(self.theme[f"icons_{icon.icon_color}_color"])

    def start(
            self,
            theme: str = "light",
            language: str = None):

        self.switch_theme(theme)
        if language and language != self.language:
            self.switch_language(language)

    def reload(self):
        self.switch_theme(self.theme_name)
        self.switch_language(self.language)

    def update_style(self, widget: DynamicWidget | str):

        if isinstance(widget, str):
            widget = self.widgets[widget]

        if not widget.styles:
            return

        extra = ""
        if widget.state in widget.styles:
            extra = self._generate_widget_style(
                widget.styles[widget.state])

        widget.setStyleSheet(f"{widget.styles['always']} {extra}")

    def set_style(
            self,
            widget: str | DynamicWidget,
            trigger: widget_trigger,
            style: str):

        widget = self.widgets[widget] if isinstance(widget, str) else widget
        widget.styles[trigger] = style
        self._widget_triggered(widget, "leave")

    def add_shortcut(
            self,
            callback: Callable,
            shortcut: str):

        try:
            keyboard.add_hotkey(shortcut, callback)
        except ValueError:
            logger.warning(f"Shortcut not set: {shortcut}")
        self.shortcuts[shortcut] = callback

    def use_preset(self, object_name: str, preset: widget_type):
        widget = self.widgets[object_name]
        widget.styles = style_presets[preset]
        self._widget_triggered(widget, "leave")

    def copy_style(
            self,
            original: str | DynamicWidget,
            copy: str | DynamicWidget):

        originalw = self.widgets[original] if isinstance(original, str) else original
        copyw = self.widgets[copy] if isinstance(copy, str) else copy
        copyw.styles = originalw.styles
        copyw.setStyleSheet(originalw.styleSheet())

    def translate(self, source: str) -> str:

        index = self.vocabulary["languages"].index(self.language)
        for translation in self.vocabulary["translations"]:
            if source in translation:
                return translation[index]
        else:
            logger.critical(f"cannot translate: {source} to {self.language}")
            raise ValueError(f"cannot translate: {source} to {self.language}")


global_widget_manager = Global()


class StylePresets(TypedDict):

    window: dict[widget_trigger, str]
    popup_sea: dict[widget_trigger, str]
    popup_island: dict[widget_trigger, str]
    button: dict[widget_trigger, str]
    input: dict[widget_trigger, str]
    label: dict[widget_trigger, str]
    frame: dict[widget_trigger, str]
    button: dict[widget_trigger, str]


style_presets = StylePresets()

always = "border: none; border-radius: %spx; outline: none;"

style_presets["window"] = {
        "always": always % 0,
        "leave": "background-color: !back!;"
    }
style_presets["input"] = {
    "always": always % cfg.radius(),
    "leave": "background-color: !highlight3!; color: !fore!;"
}
style_presets["label"] = {
    "always": always % cfg.radius(),
    "leave": "color: !fore!;"
}
style_presets["popup_island"] = {
    "always": always % cfg.BORDER_RADUIS,
    "leave": "background-color: !back!;"
}
style_presets["popup_sea"] = {
    "always": always % 0,
    "leave": "background-color: !dim!;"
}
style_presets["frame"] = {
    "always": always % 0,
    "leave": ""
}
style_presets["button"] = {
    "always": always % cfg.radius(),
    "leave": "background-color: !back!; color: !fore!;",
    "hover": "background-color: !highlight2!; color: !fore!;"
}
