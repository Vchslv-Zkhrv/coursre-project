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


class Window(CWindow):

    """
    Main window with four buttons: info, minimize, maximize and close.
    After the button is clicked, emits a signal with the corresponding name /

    Основное окно с четырьмя кнопками: справка, свернуть, развернуть и закрыть.
    После щелчка по одной из кнопок излучает сигнал с тем же именем
    """

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
