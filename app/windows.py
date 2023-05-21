from typing import TypedDict, Callable

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
from .dynamic import global_widget_manager as gwm
from .floating import Floating


class WindowForms(TypedDict):

    auth: forms.AuthForm
    main: forms.MainForm
    nofile: forms.OpenSuggestion


class WindowDialogs(TypedDict):

    close_by_user: dialogs.YesNoDialog
    close_forcibly: dialogs.AlertDialog
    alert: dialogs.AlertDialog
    choice: dialogs.ChooseVariantDialog


class WindowSignals(QtCore.QObject):

    log_in = QtCore.pyqtSignal(str, str)


class Window(dynamic.DynamicWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms
    window_signals: WindowSignals
    floating: Floating

    def __init__(self, object_name: str):

        dynamic.DynamicWindow.__init__(self)
        self.floating = Floating(self)
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

        minimize.clicked.connect(lambda e: self.showMinimized())
        maximizxe.clicked.connect(lambda e: self.on_maximize())
        close.clicked.connect(lambda e: self.on_close())
        info.clicked.connect(lambda e: self.spam())
        # info.clicked.connect(lambda e: self.signals.triggered.emit("info"))
        gwm.add_shortcut(info.click, "Ctrl+H")

        title_layout.addWidget(self.toolbar, 0, 0, 1, 1)
        title_layout.addItem(shorts.HSpacer(), 0, 1, 1, 1)
        title_layout.addWidget(buttons, 0, 2, 1, 1)
        title_layout.addWidget(self.statusbar, 1, 0, 1, 3)

        shorts.GLayout(self.content)
        self.draw_forms()
        self.draw_dialogs()

    def spam(self):
        self.show_floating("hello")

    def show_floating(self, text: str):
        self.floating.show_(text)

    def draw_forms(self):
        self.forms = WindowForms()
        layout = self.content.layout()

        self.forms["auth"] = forms.AuthForm()
        self.forms["auth"].signals.triggered.connect(
            lambda trigger: self._on_auth_triggered(trigger))
        layout.addWidget(self.forms["auth"], 0, 0, 1, 1)

        self.forms["nofile"] = forms.OpenSuggestion()
        layout.addWidget(self.forms["nofile"], 0, 0, 1, 1)

        self.forms["main"] = forms.MainForm()
        layout.addWidget(self.forms["main"], 0, 0, 1, 1)

    def _on_auth_triggered(self, trigger: str):
        if trigger == "log in":
            data = self.forms["auth"].collect()
            self.window_signals.log_in.emit(data["auth-login"], data["auth-password"])

    def draw_dialogs(self):
        self.dialogs = WindowDialogs()

        self.dialogs["close_by_user"] = dialogs.YesNoDialog(
            self,
            "Приложение будет закрыто.\nВы уверены?"
        )
        self.dialogs["close_by_user"].accepted.connect(self.close)

        self.dialogs["close_forcibly"] = dialogs.AlertDialog(self, "")
        self.dialogs["close_forcibly"].rejected.connect(self.close)

        self.dialogs["alert"] = dialogs.AlertDialog(self, "")
        self.dialogs["choice"] = dialogs.ChooseVariantDialog(self, "", "")

    def show_choice_dialog(
            self,
            title: str,
            desctiption: str,
            callback: Callable,
            items: dict[str, str],
            item_icon: str,
            translate: bool = False):

        variants = {}
        for name, text in items.items():
            button = widgets.SvgTextButton(item_icon, text)
            button.dont_translate = not translate
            button.label.label.setWordWrap(False)
            gwm.add_widget(button, style_preset="button")
            variants[name] = button

        dialog = self.dialogs["choice"]
        dialog.title.setText(title)
        dialog.message.setText(desctiption)
        dialog.load_variants(variants)
        try:
            dialog.choice_signals.choice.disconnect()
            dialog.rejected.disconnect()
        except TypeError:
            pass
        dialog.choice_signals.choice.connect(callback)
        self._check_nested_dialogs(dialog)
        dialog.show()

    def show_suspisious_error(self):
        dialog = self.dialogs["close_forcibly"]
        dialog.description.setText(
            "Данные неверны.\n\nПревышено максимальное количество попыток.\nПриложение будет закрыто."
        )
        self._check_nested_dialogs(dialog)
        dialog.show()

    def on_close(self):
        self.dialogs["close_by_user"].show()

    def on_maximize(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def show_log_in_error(self, attempt_count: int):

        if attempt_count == 3:
            message = "Данные неверны.\nОсталось три попытки."
        if attempt_count == 2:
            message = "Данные неверны.\nОсталось две попытки."
        elif attempt_count == 1:
            message = "Данные неверны.\nОсталась последняя попытка."

        self.show_alert_dialog("Предупреждение", message)

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
            self.show_alert_dialog(
                "Подсказка",
                "Введите данные вашей учетной записи, чтобы продолжить"
            )

    def _check_nested_dialogs(self, top_dialog: dialogs.Dialog):
        dd = self.toolbar.active_dropdown
        if dd:
            top_dialog.set_previous(dd)

    def show_alert_dialog(self, title: str, message: str):
        dialog = self.dialogs["alert"]
        dialog.title.setText(title)
        dialog.description.setText(message)
        self._check_nested_dialogs(dialog)
        dialog.show()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        logger.debug(f"show {self.objectName()} window")
        return super().showEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(f"close {self.objectName()} window")
        return super().closeEvent(a0)
