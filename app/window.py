from PyQt6 import QtGui, QtWidgets, QtCore

from .cwindow import CWindow, modes
from . import qt_shortcuts as shorts
from . import widgets
from . import config as cfg
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

    def __init__(self, parent: QtWidgets.QWidget = None):
        self.signals = events.WindowSignals()
        self.titlebar_height = 46
        CWindow.__init__(self, parent)
        # настройки жестов окна
        self.gesture_mode = modes.GestureResizeModes.acceptable
        self.gesture_orientation_mode = modes.ScreenOrientationModes.no_difference
        self.gesture_sides = modes.SideUsingModes.ignore_corners
        # макет шапки окна
        self.title_bar.setContentsMargins(8, 8, 8, 0)
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


class AbstractDialog(QtWidgets.QDialog):

    """
    Main application dialog template.
    Blurs the parent window when showed.
    Displayed in the center of the window. /

    Основной шаблон диалога приложения.
    Размывает родительское окно при появлении.
    Отображается в центре окна.
    """

    def __init__(self, window: AbstractWindow):

        # первоначальные настройки
        QtWidgets.QDialog.__init__(self)
        self.window_ = window
        self.setModal(True)

        # настройки внешнего вида
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        br, bg, bb, ba = cfg.CURRENT_THEME["back"].getRgb()
        fr, fg, fb, fa = cfg.CURRENT_THEME["fore"].getRgb()
        layout = shorts.GLayout(self)
        self.content = QtWidgets.QFrame()
        self.content.setStyleSheet(f"""
            background-color: rgb({br}, {bg}, {bb});
            border: 2px solid rgb({fr}, {fg}, {fb});
            border-radius: 16px;
        """)
        layout.addWidget(self.content)

    def show(self) -> None:
        self.window_.glass.show()
        center = self.window_.geometry().center()
        x = center.x() - int(self.width() / 2)
        y = center.y() - int(self.height() / 2)
        self.move(x, y)
        return super().show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_.glass.hide()
        return super().closeEvent(a0)
