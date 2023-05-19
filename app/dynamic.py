from typing import Literal, TypedDict

from PyQt6 import QtWidgets, QtGui, QtCore, QtSvg
from .cwindow import CWindow

from . import config as cfg
from . import shorts


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

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.signals = DynamicWidgetSignals()
        self.styles = {}
        self.state = "leave"


class DynamicLabel(QtWidgets.QLabel, DynamicWidget):
    pass


class DynamicSvg(QtWidgets.QLabel, DynamicWidget):

    icon_color: str
    icon_name: str

    def __init__(
            self,
            icon_name: str,
            icon_color: str,
            size: QtCore.QSize = cfg.ICONS_SIZE):

        DynamicWidget.__init__(self)
        QtWidgets.QLabel.__init__(self)
        self.icon_name = icon_name
        self.setFixedSize(size)
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.draw_icon(icon_color)
        self.setStyleSheet(
            f"border-radius: {cfg.radius()}px; background-color: none;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        global_widget_manager.add_widget(self)

    def draw_icon(self, icon_color: str):
        self.icon_color = icon_color
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
    shortcuts: list[DynamicWidget, widget_trigger, str] = []

    def __init__(self):

        self.last_autogenerated_object_name = 0
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
        self.theme_name = key

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
        if trigger in widget.styles:
            widget.state = trigger
            self._update_widget_style(widget)

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

    def update_theme(self, name: str):
        old_theme = self.theme
        self.theme = self.themes[name]
        for widget in self.widgets.values():
            if isinstance(widget, DynamicSvg) and hasattr(widget, "icon_color"):
                for cname, cvalue in old_theme.items():
                    if cvalue == widget.icon_color:
                        widget.draw_icon(self.theme[cname])
                        break
            else:
                self._update_widget_style(widget)

    def _update_widget_style(self, widget: DynamicWidget):

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
