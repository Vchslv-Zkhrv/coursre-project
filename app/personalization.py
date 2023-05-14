from dataclasses import dataclass
from typing import TypedDict, Literal

from PyQt6.QtGui import QColor
from PyQt6 import QtGui, QtWidgets

from .events import WidgetSignals, PersonalizationSignals


def rgba(color: QColor):
    r, g, b, a = color.getRgb()
    return f"rgba({r}, {g}, {b}, {a})"


icons_color = Literal["black", "white"]
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
    "icons_main_color",
    "icons_alter_color"
]
style_name = Literal[
    "color",
    "background-color",
    "border",
    "border-radius",
    "outline",
    "padding-right",
    "padding-left"
]


class Theme(TypedDict):
    dim: QColor
    fore: QColor
    back: QColor
    highlight1: QColor
    highlight2: QColor
    red: QColor
    yellow: QColor
    green: QColor
    blue: QColor
    icons_main_color: icons_color
    icons_alter_color: icons_color


light_theme = Theme()
light_theme["dim"] = QColor(0, 0, 0, 25)
light_theme["back"] = QColor(255, 255, 255)
light_theme["fore"] = QColor(30, 30, 30)
light_theme["highlight1"] = QColor(245, 245, 245)
light_theme["highlight2"] = QColor(235, 235, 235)
light_theme["red"] = QColor(255, 61, 61)
light_theme["yellow"] = QColor(255, 160, 32)
light_theme["green"] = QColor(32, 213, 32)
light_theme["blue"] = QColor(36, 138, 255)
light_theme["icons_main_color"] = "black"
light_theme["icons_alter_color"] = "white"

dark_theme = Theme()
dark_theme["dim"] = QColor(255, 255, 255, 25)
dark_theme["back"] = QColor(5, 5, 5)
dark_theme["fore"] = QColor(255, 255, 255)
dark_theme["highlight1"] = QColor(15, 15, 15)
dark_theme["highlight2"] = QColor(30, 30, 30)
dark_theme["red"] = QColor(255, 61, 61)
dark_theme["yellow"] = QColor(255, 160, 32)
dark_theme["green"] = QColor(32, 213, 32)
dark_theme["blue"] = QColor(36, 138, 255)
dark_theme["icons_main_color"] = "white"
dark_theme["icons_alter_color"] = "black"


class ApllicationThemes(TypedDict):

    light: Theme
    dark: Theme


Themes = ApllicationThemes()
Themes["dark"] = dark_theme
Themes["light"] = light_theme


CURRENT_THEME = Themes["light"]


class Style():

    """
    Style object. Can be updated during the application runtime /
    Объект стиля. Может быть обновлен во время работы приложения
    """
    unmutable: str
    mutable: dict[style_name, color_name]
    theme: Theme = CURRENT_THEME

    def __init__(
            self,
            unmutable: str,
            mutable: dict[style_name, color_name]):

        self.unmutable = unmutable
        self.mutable = mutable

    def generate(self) -> str:
        style = self.unmutable
        for key, cname in self.mutable.items():
            color = self.theme[cname]
            style += f"\n{key}: {rgba(color)};"
        return style

    def __call__(self) -> str:
        return self.generate()

    def _value(self, key) -> str:
        if key in self.settings:
            val = self.theme[self.settings[key]]
            if isinstance(val, QColor):
                return rgba(val)
            if isinstance(val, int):
                return f"{val}px"
            else:
                return str(val)
        else:
            return "none"


class ThemeSwitcher(QtWidgets.QWidget):

    theme_name: Literal["dark", "light"] = "light"

    def __init__(self):
        self.signals = PersonalizationSignals()

    def switch_theme(self, name: Literal["dark", "light"]):
        self.theme_name = name
        global CURRENT_THEME
        CURRENT_THEME = Themes[name]
        self.repeat()

    def repeat(self):
        self.signals.switch_theme.emit(self.theme_name)


theme_switcher = ThemeSwitcher()


def personalization(*styles_: tuple[str, dict[style_name, color_name]]):

    def decorator(cls: QtWidgets.QWidget):

        class ThemeWrapper(cls):

            styles: tuple[Style] = tuple(
                Style(*s) for s in styles_)

            current_state: int = 0
            theme_name: Literal["dark", "light"] = "light"

            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                self.widget_signals = WidgetSignals()
                self.widget_signals.set_state.connect(
                    lambda index: self.choose_theme(index))
                theme_switcher.signals.switch_theme.connect(
                        lambda name: self.set_theme(name))

            def choose_theme(self, index: int):
                self.current_state = index
                self.setStyleSheet(self.styles[self.current_state]())

            def set_theme(self, name: Literal["dark", "light"]):
                self.theme_name = name
                for style in self.styles:
                    style.theme = Themes[name]
                self.setStyleSheet(self.styles[self.current_state]())

            def showEvent(self, a0):
                if self.styles[self.current_state].theme != CURRENT_THEME:
                    name = "light" if self.theme_name == "dark" else "dark"
                    self.set_theme(name)
                self.setStyleSheet(self.styles[self.current_state]())
                return super().showEvent(a0)

        return ThemeWrapper

    return decorator


def parse_theme(widget: QtWidgets.QWidget) -> dict[color_name, str]:
    style = {}
    theme: Theme = widget.styles[widget.current_state].theme
    for key, value in theme.items():
        if isinstance(value, QColor):
            style[key] = rgba(value)
        else:
            style[key] = value
    return style
