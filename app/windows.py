from typing import TypedDict

from PyQt6 import QtWidgets, QtCore, QtGui
from loguru import logger

from . import shorts
from . import dialogs
from . import forms
from . import groups
from .config import FORMS
from .toolbar import ToolBar
from . import config as cfg
from .cwindow import CWindow, modes
from . import dynamic
from .config import GAP, BUTTONS_SIZE


class WindowForms(TypedDict):

    auth: forms.AuthForm
    main: forms.MainForm
    nofile: forms.OpenSuggestion


class Window(CWindow, dynamic.DynamicWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms

    def __init__(self):

        dynamic.DynamicWindow.__init__(self, "main")
        CWindow.__init__(self)

        self.titlebar_height = BUTTONS_SIZE.height() + GAP + 1
        # настройки жестов окна
        self.gesture_mode = modes.GestureResizeModes.acceptable
        self.gesture_orientation_mode = modes.ScreenOrientationModes.no_difference
        self.gesture_sides = modes.SideUsingModes.ignore_corners

        self.title_bar.setContentsMargins(GAP, GAP, GAP, 0)
        layout = shorts.HLayout(self.title_bar)
        layout.setDirection(QtWidgets.QBoxLayout.Direction.RightToLeft)
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        self.setMinimumSize(720, 480)
        shorts.GLayout(self.content)

        self.forms = WindowForms()
        self.forms["auth"] = forms.AuthForm()
        # self.forms["main"] = forms.MainForm()
        # self.forms["nofile"] = forms.OpenSuggestion(self)

        self._draw_interface()

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

    def _draw_interface(self):

        # self.toolbar = ToolBar(self)
        # self.title_bar.layout().addWidget(self.toolbar)
        # self.toolbar.signals.button_clicked.connect(
        #     lambda name: self._on_toolbar_button_click(name))

        # self.second_titlebar = groups.SecondToolbar(self)
        # self.content.layout().addWidget(self.second_titlebar, 0, 0, 1, 1)

        self.container = groups.Group("main window container")
        # self.container.setSizePolicy(shorts.ExpandingPolicy())
        # self.content.layout().addWidget(self.container, 1, 0, 1, 1)
        layout = shorts.GLayout(self.container)

        layout.addWidget(self.forms["auth"], 0, 0, 1, 1)
        # layout.addWidget(self.forms["main"], 0, 0, 1, 1)
        # layout.addWidget(self.forms["nofile"], 0, 0, 1, 1)
        self.show_form(None)

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
