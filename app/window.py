from PyQt6 import QtGui, QtWidgets, QtCore

from .cwindow import CWindow, modes
from . import qt_shortcuts as shorts
from . import widgets
from . import config as cfg

"""
Module with application window templates /
Модуль с макетами окон приложения
"""


class Window(CWindow):

    """
    Main window with three buttons: minimize, maximize and close /
    Основное окно с тремя кнопками: свернуть, развернуть и закрыть
    """

    def __init__(self, parent: QtWidgets.QWidget = None):
        self.titlebar_height = 46
        CWindow.__init__(self, parent)
        # настройки жестов окна
        self.gesture_mode = modes.GestureResizeModes.acceptable
        self.gesture_orientation_mode = modes.ScreenOrientationModes.no_difference
        self.gesture_sides = modes.SideUsingModes.ignore_corners
        # макет шапки окна
        self.title_bar.setContentsMargins(8, 8, 8, 0)
        layout = shorts.HLayout(self.title_bar)
        layout.setSpacing(2)
        layout.setDirection(QtWidgets.QBoxLayout.Direction.RightToLeft)
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        # базовые кнопки
        close = widgets.ColorButton("cross", cfg.RED)
        maximize = widgets.ColorButton("window-maximize", cfg.ORANGE)
        minimize = widgets.ColorButton("window-minimize", cfg.GREEN)
        info = widgets.ColorButton("circle-info", cfg.BLUE)
        self.title_bar.layout().addWidget(close)
        self.title_bar.layout().addWidget(maximize)
        self.title_bar.layout().addWidget(minimize)
        self.title_bar.layout().addWidget(info)
