from typing import Literal, TypedDict

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor

from .events import GlobalSignals, WidgetSignals
from . import config as cfg


def rgba(color: QColor):
    r, g, b, a = color.getRgb()
    return f"rgba({r}, {g}, {b}, {a})"


color_name = Literal[
    "!dim!",
    "!fore!",
    "!back!",
    "!highlight1!",
    "!highlight2!",
    "!red!",
    "!yellow!",
    "!green!",
    "!blue!",
    "!hotkeys!"
]


class Theme(TypedDict):
    dim: QColor
    fore: QColor
    back: QColor
    highlight1: QColor
    highlight2: QColor
    hotkeys: QColor
    red: QColor
    yellow: QColor
    green: QColor
    blue: QColor
    icons_main_color: str
    icons_alter_color: str


def parse_config_themes() -> dict[str, Theme]:
    themes = {}
    for name, colors in cfg.THEMES.items():
        colors_ = {}
        for key, value in colors.items():
            if isinstance(value, tuple):
                print(value)
                colors_[key] = QColor(*value)
            else:
                colors_[key] = value
        themes[name] = colors_
    return themes


style_item = dict[str, color_name | str]
widget_state = Literal["main", "hover", "active", "active_hover"]


class WidgetStates(TypedDict):

    main: style_item
    hover: style_item
    active: style_item
    active_hover: style_item


class DynamicWidget(QtWidgets.QWidget):

    signals: WidgetSignals

    unmutable_style: str = ""
    mutable_styles: WidgetStates
    current_state: widget_state = "main"


class NonUniqueObjectNameError(Exception):
    pass


class Global():

    """
    Global virtual object that allows widgets managing /
    Глобальный виртуальный объект, который позволяет управлять виджетами
    """

    widgets: dict[str, DynamicWidget]
    themes: dict[str, Theme]
    theme: Theme

    def __init__(self):

        self.signals = GlobalSignals()
        self.themes = parse_config_themes()

        if "main" in self.themes:
            key ="main"
        elif "light" in self.themes:
            key = "light"
        else:
            key = sorted(tuple(self.themes.keys()))[0]

        self.theme = self.themes[key]

    def add_widget(
            self,
            object_name: str,
            widget: DynamicWidget):

        """
        Adds widget to global heap. \
        Добавляет виджет в глобальный набор
        """

        if object_name in self.widgets:
            raise NonUniqueObjectNameError

        widget.setObjectName(object_name)
        self.widgets[object_name] = widget
        widget.signals.triggered.connect(
            lambda trigger: self._widget_triggered(widget, trigger))

    def _widget_triggered(self, widget: DynamicWidget, trigger: widget_state):
        try:
            widget.current_state = trigger
            self._update_widget_style(widget)
        except KeyError:
            print(f"widget {widget.objectName()} has no {trigger} style")

    def _generate_widget_style(self, style: style_item) -> str:
        stylesheet = ""
        for key, value in style.items():
            stylesheet += f"{key}: {value};\n"
        return self._replace_stylesheet(stylesheet)

    def _replace_stylesheet(self, stylesheet: str) -> str:
        stylesheet = self._replace_stylesheet(stylesheet)
        before, substr, *after = stylesheet.split("!")
        before = f"{before}{rgba(self.theme[substr])}"
        after = "!".join(after)
        if "!" in after:
            after = self._replace_stylesheet(after)
        return before + after

    def update_theme(self, name: str):
        self.theme = self.themes[name]
        for widget in self.widgets.values():
            self._update_widget_style(widget)

    def _update_widget_style(self, widget: DynamicWidget):
        widget.setStyleSheet(
            widget.unmutable_style +
            self._generate_widget_style(
                widget.mutable_styles[widget.current_state]))

    def set_style(
            self,
            object_name: str,
            trigger: widget_state,
            style: style_item):

        widget = self.widgets[object_name]
        widget.mutable_styles[trigger] = style


global_widget_manager = Global()
