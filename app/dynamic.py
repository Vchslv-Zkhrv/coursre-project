from typing import Literal, TypedDict

from PyQt6 import QtWidgets, QtGui, QtCore

from . import config as cfg


def rgba(color: QtGui.QColor):
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
            if isinstance(value, tuple):
                print(value)
                colors_[key] = QtGui.QColor(*value)
            else:
                colors_[key] = value
        themes[name] = colors_
    return themes


style_item = dict[str, color_name | str]
widget_trigger = Literal["main", "hover", "active", "active_hover", "hotkey", "click"]


class WidgetStates(TypedDict):

    main: style_item
    hover: style_item
    active: style_item
    active_hover: style_item


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

    signals: DynamicWidgetSignals = DynamicWidgetSignals()

    unmutable_style: str = ""
    mutable_styles: WidgetStates = WidgetStates()
    current_state: widget_trigger = "main"

    def __init__(self, object_name: str):
        QtWidgets.QWidget.__init__(self)
        self.setObjectName(object_name)


class DynamicLabel(QtWidgets.QLabel, DynamicWidget):
    pass


class DynamicButton(QtWidgets.QPushButton, DynamicWidget):

    def __init__(self, object_name: str):
        self.hovered = False
        QtWidgets.QPushButton.__init__(self)
        DynamicWidget.__init__(self, object_name)
        self.signals
        self.clicked.connect(lambda e: self.signals.triggered.emit("click"))

    def _set_hovered(self, hovered: bool):
        self.signals.blockSignals(True)
        if hovered:
            self.signals.triggered.emit("hover")
        else:
            self.signals.triggered.emit("leave")
        self.signals.blockSignals(False)

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


class DynamicWindow(QtWidgets.QMainWindow, DynamicWidget):
    pass

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


class Global():

    """
    Global virtual object that allows widgets managing /
    Глобальный виртуальный объект, который позволяет управлять виджетами
    """

    widgets: dict[str, DynamicWidget]
    themes: dict[str, Theme]
    theme: Theme
    window: DynamicWindow = None
    shortcuts: list[DynamicWidget, widget_trigger, str] = []

    def __init__(self):

        self.signals = GlobalSignals()
        self.themes = parse_config_themes()
        self.widgets = {}

        if "main" in self.themes:
            key = "main"
        elif "light" in self.themes:
            key = "light"
        else:
            key = sorted(tuple(self.themes.keys()))[0]

        self.theme = self.themes[key]

    def add_widget(
            self,
            widget: DynamicWidget):

        """
        Adds widget to global heap. \
        Добавляет виджет в глобальный набор
        """

        object_name = widget.objectName()

        if object_name in self.widgets:
            raise NonUniqueObjectNameError

        widget.setObjectName(object_name)
        self.widgets[object_name] = widget
        widget.signals.triggered.connect(
            lambda trigger: self._widget_triggered(widget, trigger))

    def _widget_triggered(self, widget: DynamicWidget, trigger: widget_trigger):
        widget.current_state = trigger
        print(trigger, widget)
        try:
            self._update_widget_style(widget)
        except (KeyError, TypeError):
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
            trigger: widget_trigger,
            style: style_item):

        widget = self.widgets[object_name]
        widget.mutable_styles[trigger] = style

    def add_shortcut(
            self,
            object_name: str,
            shortcut: str,
            trigger: widget_trigger = "click"):

        self.shortcuts.append((self.widgets[object_name], trigger, shortcut))

    def _update_shortcuts(self):
        for widget, trigger, shortcut in self.shortcuts:
            QtGui.QShortcut(
                shortcut,
                self.window
            ).activated.connect(lambda t=trigger, w=widget: w.signals.triggered.emit(t))

    def set_window(self, window: DynamicWindow):
        self.window = window
        self._update_shortcuts()


global_widget_manager = Global()
