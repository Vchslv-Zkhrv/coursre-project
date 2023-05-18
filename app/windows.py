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


class AbstractWindow(CWindow, dynamic.DynamicWindow):

    """
    Main window with four buttons: info, minimize, maximize and close.
    After the button is clicked, emits a signal with the corresponding name /

    Основное окно с четырьмя кнопками: справка, свернуть, развернуть и закрыть.
    После щелчка по одной из кнопок излучает сигнал с тем же именем
    """

    _is_narrow: bool = False

    def __init__(
            self,
            object_name: str,
            parent: QtWidgets.QWidget = None):

        self.titlebar_height = BUTTONS_SIZE.height() + GAP + 1
        dynamic.DynamicWindow.__init__(self, object_name)
        CWindow.__init__(self, parent)

        # настройки жестов окна
        self.gesture_mode = modes.GestureResizeModes.acceptable
        self.gesture_orientation_mode = modes.ScreenOrientationModes.no_difference
        self.gesture_sides = modes.SideUsingModes.ignore_corners
        # макет шапки окна
        self.title_bar.setContentsMargins(GAP, GAP, GAP, 0)
        layout = shorts.HLayout(self.title_bar)
        layout.setDirection(QtWidgets.QBoxLayout.Direction.RightToLeft)
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        # базовые кнопки
        frame = QtWidgets.QFrame()
        fl = shorts.HLayout(frame)
        fl.setSpacing(2)
        # frame.close_ = custom.getColorButton("cross", "red")
        # frame.maximize = custom.getColorButton("window-maximize", "yellow")
        # frame.minimize = custom.getColorButton("window-minimize", "green")
        # frame.info = custom.getColorButton("circle-info", "blue")
        # fl.addWidget(frame.info)
        # fl.addWidget(frame.minimize)
        # fl.addWidget(frame.maximize)
        # fl.addWidget(frame.close_)
        self.title_bar.buttons = frame
        # события, предназначенные для использования в подклассах
        self.title_bar.layout().addWidget(self.title_bar.buttons)
        # frame.info.clicked.connect(lambda e: self.signals.info.emit())
        # frame.close_.clicked.connect(lambda e: self.signals.close.emit())
        # frame.minimize.clicked.connect(lambda e: self.signals.minimize.emit())
        # frame.maximize.clicked.connect(lambda e: self.signals.maximize.emit())

    def blur(self, blur: bool):
        effect = QtWidgets.QGraphicsBlurEffect()
        if blur:
            effect.setBlurRadius(3)
        else:
            effect.setBlurRadius(0)
        self.setGraphicsEffect(effect)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        logger.debug(f"show {self.objectName()} window")
        return super().showEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.debug(f"close {self.objectName()} window")
        return super().closeEvent(a0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        narrow = self.width() <= cfg.NARROW_START
        if narrow and not self._is_narrow:
            self._is_narrow = True
        elif not narrow and self._is_narrow:
            self._is_narrow = False


class Window(AbstractWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms

    def __init__(self):
        AbstractWindow.__init__(self, "main")

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

