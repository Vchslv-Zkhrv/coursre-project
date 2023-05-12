from PyQt6 import QtWidgets, QtSvg, QtCore, QtGui

from . import config as cfg
from . import qt_shortcuts as shorts
from . import events

"""
Module with customized PyQt6 basic widgets /
Модуль с модифицированными базовыми виджетами библиотеки PyQt6

There are widgets with extended functionality and behavour /
Виджеты с расширенным функционалом и поведением

"""

state = tuple[QtWidgets.QLabel, QtGui.QColor]


class SvgLabel(QtWidgets.QLabel):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(self, icon_path: str, size: QtCore.QSize = None):
        QtWidgets.QLabel.__init__(self)
        size = size if size else cfg.ICONS_SIZE
        self.setFixedSize(size)
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.set_icon(icon_path)
        br = int(self.height() / 2)
        self.setStyleSheet(f"border-radius: {br}px; background-color: none;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def set_icon(self, icon_path: str):
        renderer = QtSvg.QSvgRenderer(icon_path)
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setPixmap(pixmap)


class SvgButton(events.HoverableButton):

    """
    QPushButton with svg icon with to states: normal and hovered /
    Виджет QPushButton с svg - иконкой и двумя состояниями: обьчное и наведенное
    """

    def __init__(
            self,
            state0: state,
            state1: state):
        events.HoverableButton.__init__(self)
        # все кнопки имеют единый стиль
        self.setFixedSize(cfg.BUTTONS_SIZE)
        br = int(self.height() / 2)
        self.style_sheet = f"color: none; border: none; border-radius: {br}px; "
        self.style_sheet += "background-color: %s; "
        # макет
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # обе иконки помещаются на макет и скрываются
        layout.addWidget(state0[0])
        layout.addWidget(state1[0])
        state0[0].hide()
        state1[0].hide()
        self.state0 = state0
        self.state1 = state1
        # текущая иконка
        self.label = QtWidgets.QLabel()
        self._set_state(state0)
        # иконка и цвет фона меняются по наведению
        self.signals.hovered.connect(lambda: self._set_state(self.state1))
        self.signals.leaved.connect(lambda: self._set_state(self.state0))

    def _set_state(self, state_: state):
        label, color = state_
        r, g, b, a = color.getRgb()
        style = self.style_sheet % f"rgb({r}, {g}, {b})"
        self.setStyleSheet(style)
        if self.label != label:
            self.label.hide()
            label.show()
            self.label = label
