from PyQt6 import QtWidgets, QtCore, QtGui

from .cwindow import CWindow

"""
Module with custom signals and handlers /
Модуль с кастомными сигналами и обработчиками
"""


class ButtonSignals(QtCore.QObject):

    """
    extra signals pack for buttons /
    пакет дополнительных сигналов для кнопок
    """

    hovered = QtCore.pyqtSignal()
    leaved = QtCore.pyqtSignal()


class WindowSignals(QtCore.QObject):

    """
    extra signals pack for windows /
    пакет дополнительных сигналов для окон
    """
    close = QtCore.pyqtSignal()
    minimize = QtCore.pyqtSignal()
    maximize = QtCore.pyqtSignal()
    info = QtCore.pyqtSignal()


class HoverableButton(QtWidgets.QPushButton):

    """
    Button emitting signals on mouse hover or leave. /
    Кнопка, излучающая сигналы при наведении или отпускании мыши.
    """

    def __init__(self):
        self.hovered = False
        QtWidgets.QPushButton.__init__(self)
        self.signals = ButtonSignals()

    def event(self, e: QtCore.QEvent) -> bool:
        if isinstance(e, QtGui.QHoverEvent):
            if e.position().x() < 0:
                hover = False
            else:
                hover = True
            if hover != self.hovered:
                if hover:
                    self.signals.hovered.emit()
                else:
                    self.signals.leaved.emit()
                self.hovered = hover
        return super().event(e)


class EventWindow(CWindow):

    """
    Window with extended signals set /
    Окно с расширенным набором сигналов
    """

    def __init__(self, parent: QtWidgets.QWidget = None):
        CWindow.__init__(self, parent)
        self.signals = WindowSignals()