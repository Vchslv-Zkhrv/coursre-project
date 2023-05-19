from typing import TypedDict

from PyQt6 import QtGui
from loguru import logger

from . import shorts
from . import dialogs
from . import forms
from . import widgets
from .config import FORMS
from .cwindow import modes
from . import dynamic
from .config import GAP, BUTTONS_SIZE
from . import titlebar


class WindowForms(TypedDict):

    auth: forms.AuthForm
    main: forms.MainForm
    nofile: forms.OpenSuggestion


class Window(dynamic.DynamicWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms

    def __init__(self, object_name: str):

        dynamic.DynamicWindow.__init__(self)

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
        close.clicked.connect(lambda e: self.close())

        title_layout.addWidget(self.toolbar, 0, 0, 1, 1)
        title_layout.addItem(shorts.HSpacer(), 0, 1, 1, 1)
        title_layout.addWidget(buttons, 0, 2, 1, 1)
        title_layout.addWidget(self.statusbar, 1, 0, 1, 3)

        layout = shorts.GLayout(self.content)
        self.forms = WindowForms()
        self.forms["auth"] = forms.AuthForm()
        # self.forms["main"] = forms.MainForm()
        # self.forms["nofile"] = forms.OpenSuggestion(self)

        layout.addWidget(self.forms["auth"], 0, 0, 1, 1)

    def _show_suspisious_error(self):
        d = dialogs.AlertDialog(
            "suspisuous log in attempt",
            self,
            "Данные неверны.\n\nПревышено максимальное количество попыток.\nПриложение будет закрыто.")
        d.show()
        d.rejected.connect(self.close())

    def on_close(self):
        d = dialogs.YesNoDialog("window closer", self, "Закрыть приложение?")
        d.island.setFixedHeight(200)
        d.accepted.connect(self.close)
        d.show()

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
        dialog = dialogs.AlertDialog(
            "wrong log in alert",
            self,
            f"Данные неверны.\n\n{message}")
        dialog.show()

    def show_form(self, name: FORMS):
        for name_, form in self.forms.items():
            if name == name_:
                form.show()
            else:
                form.hide()
        if name == "auth":
            # self.second_titlebar.hide()
            # self.toolbar.hide()
            pass
        else:
            # self.second_titlebar.show()
            # self.toolbar.show()
            pass

    def _on_toolbar_button_click(self, name: str):
        self.signals.button_click.emit(name)

    def show_help(self, mode: FORMS):
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
