from PyQt6 import QtWidgets, QtCore, QtGui


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


class AuthorizationSignals(QtCore.QObject):

    """
    extra signals pack for authorization window /
    пакет дополнительнх сигналов формы авторизации
    """

    correct = QtCore.pyqtSignal()
    incorrect = QtCore.pyqtSignal()
    suspicious = QtCore.pyqtSignal()


class FormSignals(QtCore.QObject):

    """
    extra signals pack for forms /
    пакет дополнительнх сигналов для форм
    """

    send = QtCore.pyqtSignal()


class SwitchingButtonSignals(QtCore.QObject):

    """
    extra signals pack for SwitchingButton /
    пакет дополнительнх сигналов для SwitchingButton
    """

    switched = QtCore.pyqtSignal()


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
