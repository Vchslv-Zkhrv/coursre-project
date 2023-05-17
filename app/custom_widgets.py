from typing import Literal

from PyQt6 import QtWidgets, QtSvg, QtCore, QtGui

from . import config as cfg
from . import shorts
from . import events


"""
Module with customized PyQt6 basic widgets /
Модуль с модифицированными базовыми виджетами библиотеки PyQt6

There are widgets with extended functionality and behavour /
Виджеты с расширенным функционалом и поведением

"""


class SvgLabel(QtWidgets.QLabel):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(
            self,
            icon_name: str,
            icon_color_name: Literal["icons_main_color", "icons_alter_color"] = "icons_main_color",
            size: QtCore.QSize = None):

        QtWidgets.QLabel.__init__(self)
        self.icon_name = icon_name
        size = size if size else cfg.ICONS_SIZE
        self.setFixedSize(size)
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_icon()
        self.setStyleSheet(
            f"border-radius: {cfg.radius()}px; background-color: none;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def update_icon(self):
        renderer = QtSvg.QSvgRenderer(
            cfg.icon("black", self.icon_name))
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
            label0: SvgLabel,
            label1: SvgLabel):

        events.HoverableButton.__init__(self)
        self.widget_signals = events.WidgetSignals()

        # все кнопки имеют единый стиль
        self.setFixedSize(cfg.BUTTONS_SIZE)
        # макет
        layout = shorts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # обе иконки помещаются на макет и скрываются
        layout.addWidget(label0)
        layout.addWidget(label1)
        label0.hide()
        label1.hide()
        self.label0 = label0
        self.label1 = label1
        # текущая иконка
        self._set_hovered(False)
        # иконка и цвет фона меняются по наведению
        self.signals.hovered.connect(lambda: self._set_hovered(True))
        self.signals.leaved.connect(lambda: self._set_hovered(False))

    def _set_hovered(self, hovered: bool):
        self.signals.blockSignals(True)
        if hovered:
            self.widget_signals.set_state.emit(1)
            self.label0.hide()
            self.label1.show()
        else:
            self.widget_signals.set_state.emit(0)
            self.label0.show()
            self.label1.hide()
        self.signals.blockSignals(False)
