from PyQt6 import QtGui, QtWidgets, QtCore
from loguru import logger

from .cwindow import CWindow, modes
from . import shorts
from . import widgets
from . import config as cfg
from .config import GAP, BORDER_RADUIS, BUTTONS_SIZE, CURRENT_THEME as THEME
from . import events

"""
Module with application window templates /
Модуль с макетами окон приложения
"""


class WindowGlass(QtWidgets.QMainWindow):

    """
    Semi-transparent rectangle that blurs the window /
    Полупрозрачный прямоугольник, размывающий окно
    """

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window_ = window
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool)
        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setStyleSheet("background-color: rgba(0,0,0,40)")

    def show(self) -> None:
        self.setFixedSize(self.window_.size())
        self.move(self.window_.pos())
        self.blur()
        return super().show()

    def blur(self):
        blur = QtWidgets.QGraphicsBlurEffect()
        blur.setBlurRadius(3)
        self.window_.setGraphicsEffect(blur)

    def hide(self) -> None:
        blur = QtWidgets.QGraphicsBlurEffect()
        blur.setBlurRadius(0)
        self.window_.setGraphicsEffect(blur)
        return super().hide()


class AbstractWindow(CWindow):

    """
    Main window with four buttons: info, minimize, maximize and close.
    After the button is clicked, emits a signal with the corresponding name /

    Основное окно с четырьмя кнопками: справка, свернуть, развернуть и закрыть.
    После щелчка по одной из кнопок излучает сигнал с тем же именем
    """

    signlas: events.WindowSignals
    glass: WindowGlass
    _is_narrow: bool = False

    def __init__(self, name: str, parent: QtWidgets.QWidget = None):
        self.signals = events.WindowSignals()
        self.titlebar_height = BUTTONS_SIZE.height() + GAP + 1
        CWindow.__init__(self, parent)
        self.centralWidget().setStyleSheet(f"background-color: {THEME['back']};")
        self.setObjectName(name)
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
        frame.close_ = widgets.ColorButton("cross", cfg.RED)
        frame.maximize = widgets.ColorButton("window-maximize", cfg.ORANGE)
        frame.minimize = widgets.ColorButton("window-minimize", cfg.GREEN)
        frame.info = widgets.ColorButton("circle-info", cfg.BLUE)
        fl.addWidget(frame.info)
        fl.addWidget(frame.minimize)
        fl.addWidget(frame.maximize)
        fl.addWidget(frame.close_)
        self.title_bar.buttons = frame
        # события, предназначенные для использования в подклассах
        self.title_bar.layout().addWidget(self.title_bar.buttons)
        frame.info.clicked.connect(lambda e: self.signals.info.emit())
        frame.close_.clicked.connect(lambda e: self.signals.close.emit())
        frame.minimize.clicked.connect(lambda e: self.signals.minimize.emit())
        frame.maximize.clicked.connect(lambda e: self.signals.maximize.emit())
        # размытие (применяется для отрисовки диалогов поверх окна)
        self.glass = WindowGlass(self)

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
            self.signals.narrow.emit()
        elif not narrow and self._is_narrow:
            self._is_narrow = False
            self.signals.normal.emit()


class AbstractDialog(QtWidgets.QDialog):

    """
    Main application dialog template.
    Blurs the parent window when showed.
    Displayed in the center of the window. /

    Основной шаблон диалога приложения.
    Размывает родительское окно при появлении.
    Отображается в центре окна.
    """

    def __init__(self, name: str, window: AbstractWindow):

        # первоначальные настройки
        QtWidgets.QDialog.__init__(self)
        self.setObjectName(name)
        self.window_ = window
        self.setModal(True)

        # настройки внешнего вида
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        br, bg, bb, ba = THEME["back"].getRgb()
        layout = shorts.GLayout(self)
        self.content = QtWidgets.QFrame()
        self.content.setStyleSheet(f"""
            background-color: rgb({br}, {bg}, {bb});
            border-radius: {BORDER_RADUIS}px;
        """)
        layout.addWidget(self.content)

    def accept(self) -> None:
        logger.debug(f"accept {self.objectName()} dialog")
        return super().accept()

    def reject(self) -> None:
        logger.debug(f"reject {self.objectName()} dialog")
        return super().reject()

    def show(self) -> None:
        logger.debug(f"show {self.objectName()} dialog")
        self.window_.glass.show()
        center = self.window_.geometry().center()
        x = center.x() - int(self.width() / 2)
        y = center.y() - int(self.height() / 2)
        self.move(x, y)
        return super().show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_.glass.hide()
        return super().closeEvent(a0)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.window_.glass.hide()
        return super().hideEvent(a0)


class AbstractMessage(QtWidgets.QDialog):

    """
    Popup message that dissapears on user click.
    Useful content should be placed on AbstractMessage.island frame /
    Всплывающее сообщение, исчезающее по щелчку.
    Полезная нагрузка располагается на AbstractMessage.island
    """

    def __init__(
            self,
            window: AbstractWindow,
            geometry: QtCore.QRect,
            previous: QtWidgets.QDialog = None):
        self._active = False
        self.window_ = window
        self._previous = previous
        self._next = None

        QtWidgets.QDialog.__init__(self)

        if previous:
            self._previous._next = self

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool)
        self.setGeometry(window.geometry())
        self.setModal(True)

        layout = shorts.GLayout(self)
        self.sea = QtWidgets.QPushButton()
        self.sea.setStyleSheet("color: None; border: none; background-color: rgba(0,0,0,0.01)")
        self.sea.setSizePolicy(shorts.ExpandingPolicy())
        self.sea.setText("")
        layout.addWidget(self.sea, 0, 0, 1, 1)
        self.sea.clicked.connect(lambda e: self.close())

        self.island = QtWidgets.QFrame(self)
        br, bg, bb, ba = THEME["back"].getRgb()
        self.island.setStyleSheet(f"""
            background-color: rgb({br}, {bg}, {bb});
            border: none;
            border-radius: {BORDER_RADUIS}px;
        """)
        self.island.setGeometry(geometry)

    def event(self, a0: QtCore.QEvent) -> bool:
        # единственный способ достоверно перехватить событие потери фокуса
        if not self._next:
            t = int(str(a0.type()))
            if t == 99:
                if self._active:
                    self.close()
                else:
                    self._active = True
        return super().event(a0)

    def show(self) -> None:
        self.window_.glass.show()
        center = self.window_.geometry().center()
        x = center.x() - int(self.width() / 2)
        y = center.y() - int(self.height() / 2)
        self.move(x, y)
        if self._previous:
            self._previous._active = False
            opacity = QtWidgets.QGraphicsOpacityEffect()
            opacity.setOpacity(0.5)
            self._previous.setGraphicsEffect(opacity)
        super().show()
        self.activateWindow()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_.glass.hide()
        if self._previous:
            self._previous.close()
        return super().closeEvent(a0)
