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
    narrow = QtCore.pyqtSignal()
    normal = QtCore.pyqtSignal()
    button_click = QtCore.pyqtSignal(str)


class AuthorizationSignals(QtCore.QObject):

    """
    extra signals pack for authorization window /
    пакет дополнительнх сигналов формы авторизации
    """

    correct = QtCore.pyqtSignal()
    incorrect = QtCore.pyqtSignal(int)
    suspicious = QtCore.pyqtSignal()


class FormSignals(QtCore.QObject):

    """
    extra signals pack for forms /
    пакет дополнительнх сигналов для форм
    """

    send = QtCore.pyqtSignal(dict)


class ToolbarEvents(QtCore.QObject):

    """
    extra signals pack for toolbar /
    пакет дополнительнх сигналов для toolbar
    """

    button_clicked = QtCore.pyqtSignal(str)


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
        self.widget_signals = WidgetSignals()
        self.signals.hovered.connect(lambda: self._set_hovered(True))
        self.signals.leaved.connect(lambda: self._set_hovered(False))

    def _set_hovered(self, hovered: bool):
        self.signals.blockSignals(True)
        if hovered:
            self.widget_signals.set_state.emit(1)
        else:
            self.widget_signals.set_state.emit(0)
        self.signals.blockSignals(False)

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

    def set_shortcut(self, hotkey: str, window: QtWidgets.QMainWindow):
        QtGui.QShortcut(hotkey, window).activated.connect(self.clicked.emit)


class PersonalizationSignals(QtCore.QObject):

    """
    extra signal that can applied to widget to update
    it's personalization on application runtime /
    дополнительный сигнал, который может быть применен к виджету,
    чтобы обновлять его внешний вид во время работы приложения
    """

    switch_theme = QtCore.pyqtSignal(str)


class WidgetSignals(QtCore.QObject):

    set_state = QtCore.pyqtSignal(int)


class ChoiceSignals(QtCore.QObject):

    choice = QtCore.pyqtSignal(str)


class RadioGroupSignals(QtCore.QObject):

    radio_click = QtCore.pyqtSignal(int)


class RadioButtonSignals(QtCore.QObject):

    clicked = QtCore.pyqtSignal(bool)
