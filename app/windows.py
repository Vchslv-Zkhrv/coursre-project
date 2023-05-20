from typing import TypedDict

from PyQt6 import QtGui, QtCore
from loguru import logger

from . import shorts
from . import dialogs
from . import forms
from . import widgets
from .cwindow import modes
from . import dynamic
from .config import GAP, BUTTONS_SIZE
from . import titlebar


class WindowForms(TypedDict):

    auth: forms.AuthForm
    main: forms.MainForm
    nofile: forms.OpenSuggestion


class WindowDialogs(TypedDict):

    closer: dialogs.YesNoDialog
    log_in_error: dialogs.AlertDialog
    log_in_block: dialogs.AlertDialog


class WindowSignals(QtCore.QObject):

    log_in = QtCore.pyqtSignal(str, str)


class Window(dynamic.DynamicWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms
    window_signals: WindowSignals

    def __init__(self, object_name: str):

        dynamic.DynamicWindow.__init__(self)
        self.window_signals = WindowSignals()
        self.setObjectName(object_name)
        self.setMinimumSize(1080, 720)

        self.gesture_mode = modes.GestureResizeModes.acceptable
        self.gesture_orientation_mode = modes.ScreenOrientationModes.no_difference
        self.gesture_sides = modes.SideUsingModes.ignore_corners

        self.titlebar_height = BUTTONS_SIZE.height()*2 + GAP*3
        self.title_bar.setFixedHeight(self.titlebar_height)
        self.title_bar.setContentsMargins(GAP, GAP, GAP, GAP)
        title_layout = shorts.GLayout(self.title_bar)
        title_layout.setSpacing(GAP)

        self.toolbar = titlebar.ToolBar(self)
        self.statusbar = titlebar.StatusBar(self)

        buttons = dynamic.DynamicFrame()
        buttons_layout = shorts.HLayout(buttons)
        buttons_layout.setSpacing(GAP)

        close = widgets.get_color_button(
            f"{object_name}-close-button",
            "cross",
            "red"
        )
        maximizxe = widgets.get_color_button(
            f"{object_name}-max-button",
            "window-maximize",
            "yellow"
        )
        minimize = widgets.get_color_button(
            f"{object_name}-min-button",
            "window-minimize",
            "green"
        )
        info = widgets.get_color_button(
            f"{object_name}-info-button",
            "circle-info",
            "blue"
        )

        buttons_layout.addWidget(info)
        buttons_layout.addWidget(minimize)
        buttons_layout.addWidget(maximizxe)
        buttons_layout.addWidget(close)

        info.clicked.connect(lambda e: self.signals.triggered.emit("info"))
        minimize.clicked.connect(lambda e: self.showMinimized())
        maximizxe.clicked.connect(lambda e: self.on_maximize())
        close.clicked.connect(lambda e: self.on_close())

        title_layout.addWidget(self.toolbar, 0, 0, 1, 1)
        title_layout.addItem(shorts.HSpacer(), 0, 1, 1, 1)
        title_layout.addWidget(buttons, 0, 2, 1, 1)
        title_layout.addWidget(self.statusbar, 1, 0, 1, 3)

        shorts.GLayout(self.content)
        self.draw_forms()
        self.draw_dialogs()

    def draw_forms(self):
        self.forms = WindowForms()
        layout = self.content.layout()

        self.forms["auth"] = forms.AuthForm()
        self.forms["auth"].signals.triggered.connect(
            lambda trigger: self._on_auth_triggered(trigger))
        layout.addWidget(self.forms["auth"], 0, 0, 1, 1)

        self.forms["nofile"] = forms.OpenSuggestion()
        layout.addWidget(self.forms["nofile"], 0, 0, 1, 1)

    def _on_auth_triggered(self, trigger: str):
        if trigger == "log in":
            data = self.forms["auth"].collect()
            self.window_signals.log_in.emit(data["auth-login"], data["auth-password"])

    def draw_dialogs(self):
        self.dialogs = WindowDialogs()

        self.dialogs["closer"] = dialogs.YesNoDialog(
            self,
            "Приложение будет закрыто.\nВы уверены?"
        )
        self.dialogs["closer"].accepted.connect(self.close)

        self.dialogs["log_in_error"] = dialogs.AlertDialog(self, "")
        self.dialogs["log_in_block"] = dialogs.AlertDialog(self, "")

    def _show_suspisious_error(self):
        dialog = self.dialogs["log_in_block"]
        dialog.description.setText(
            "Данные неверны.\n\nПревышено максимальное количество попыток.\nПриложение будет закрыто."
        )
        dialog.show()
        dialog.rejected.connect(self.close())

    def on_close(self):
        self.dialogs["closer"].show()

    def on_maximize(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def _show_log_in_error(self, attempt_count: int):
        if attempt_count in (2, 3):
            message = f"Осталось {attempt_count} попытки"
        elif attempt_count == 1:
            message = "Осталась последняя попытка"
        self.dialogs["log_in_error"].description.setText(
            f"Данные неверны.\n{message}")
        self.dialogs["log_in_error"].show()

    def show_form(self, name: str):
        for name_, form in self.forms.items():
            if name == name_:
                form.show()
            else:
                form.hide()
        if name == "auth":
            self.forms["auth"].login.setFocus()

    def _on_toolbar_button_click(self, name: str):
        self.signals.button_click.emit(name)

    def show_help(self, mode: str):
        if mode == "auth":
            dialog = dialogs.AlertDialog(
                "info-auth",
                self,
                "Введите данные вашей учетной записи, чтобы продолжить")
            dialog.title.setText("Подсказка")
            dialog.show()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        logger.debug(f"show {self.objectName()} window")
        return super().showEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(f"close {self.objectName()} window")
        return super().closeEvent(a0)
