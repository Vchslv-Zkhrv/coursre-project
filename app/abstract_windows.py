from PyQt6 import QtGui, QtWidgets, QtCore
from loguru import logger

from .cwindow import CWindow, modes
from . import shorts
from . import config as cfg
from .config import GAP, BUTTONS_SIZE
from . import dynamic


"""
Module with application window templates /
Модуль с макетами окон приложения
"""


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


class AbstractPopup(dynamic.DynamicDialog):

    """
    Base class for popups.
    Blurs and dims the parent window when showed. /
    Базовый класс для всплывающих окон.
    Размывает и затемняет родительское окно при появлении
    """

    def __init__(
            self,
            object_name: str,
            window: AbstractWindow,
            previous: QtWidgets.QDialog = None):

        self.window_ = window
        self._previous = previous
        self._next = None

        dynamic.DynamicDialog.__init__(self, object_name)

        if previous:
            self._previous._next = self

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool)
        self.setModal(True)

        layout = shorts.GLayout(self)

        self.sea = QtWidgets.QPushButton()
        self.sea.setSizePolicy(shorts.ExpandingPolicy())
        self.sea.setText("")
        layout.addWidget(self.sea, 0, 0, 1, 1)

        self.island = QtWidgets.QFrame(self)

    def show_(self, geo: QtCore.QRect):
        self.island.setGeometry(geo)
        self.show()

    def show(self) -> None:
        self.update_style()
        self.setGeometry(self.window_.geometry())
        self.window_.blur(True)
        if self._previous:
            self._previous._active = False
            opacity = QtWidgets.QGraphicsOpacityEffect()
            opacity.setOpacity(0.5)
            self._previous.setGraphicsEffect(opacity)
        super().show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_.blur(False)
        if self._previous:
            self._previous.close()
        return super().closeEvent(a0)


class AbstractDialog(AbstractPopup):

    """
    Main application dialog template.
    Displayed in the center of the window. /

    Основной шаблон диалога приложения.
    Отображается в центре окна.
    """

    def __init__(
            self,
            object_name: str,
            window: AbstractWindow):

        # первоначальные настройки
        AbstractPopup.__init__(self, object_name, window)

    def accept(self) -> None:
        logger.debug(f"accept {self.objectName()} dialog")
        return super().accept()

    def reject(self) -> None:
        logger.debug(f"reject {self.objectName()} dialog")
        return super().reject()

    def show(self) -> None:
        super().show()
        logger.debug(f"show {self.objectName()} dialog")
        center = self.sea.geometry().center()
        x = center.x() - int(self.island.width() / 2)
        y = center.y() - int(self.island.height() / 2)
        self.island.move(x, y)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_.blur(False)
        return super().closeEvent(a0)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.window_.blur(False)
        return super().hideEvent(a0)


class AbstractMessage(AbstractPopup):

    """
    Popup message that dissapears on user click /
    Всплывающее сообщение, исчезающее по щелчку.
    """

    def __init__(
            self,
            object_name: str,
            window: AbstractWindow,
            previous: QtWidgets.QDialog = None):

        AbstractPopup.__init__(self, object_name, window, previous)
        self.sea.clicked.connect(lambda e: self.close())

    def show_(self, geo: QtCore.QRect):
        self.island.setGeometry(geo)
        self.show()
