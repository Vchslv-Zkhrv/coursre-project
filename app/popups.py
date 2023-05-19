from PyQt6 import QtGui, QtWidgets, QtCore
from loguru import logger

from . import shorts
from . import dynamic
from .dynamic import global_widget_manager as gwm

"""
Module with application window templates /
Модуль с макетами окон приложения
"""


class Popup(dynamic.DynamicDialog):

    """
    Base class for popups.
    Blurs and dims the parent window when showed. /
    Базовый класс для всплывающих окон.
    Размывает и затемняет родительское окно при появлении
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            previous: QtWidgets.QDialog = None):

        self.window_ = window
        self._previous = previous
        self._next = None

        dynamic.DynamicDialog.__init__(self)
        self.setObjectName(object_name)

        if previous:
            self._previous._next = self

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool)
        self.setModal(True)

        layout = shorts.GLayout(self)

        self.sea = dynamic.DynamicButton()
        self.sea.setSizePolicy(shorts.ExpandingPolicy())
        self.sea.setText("")
        gwm.add_widget(self.sea, f"{object_name}-sea", "popup_sea")

        layout.addWidget(self.sea, 0, 0, 1, 1)
        self.island = dynamic.DynamicFrame()
        self.island.setParent(self)
        gwm.add_widget(self.island, f"{object_name}-island", "popup_island")

    def show_(self, geo: QtCore.QRect):
        self.island.setGeometry(geo)
        self.show()

    def show(self) -> None:
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


class Dialog(Popup):

    """
    Main application dialog template.
    Displayed in the center of the window. /

    Основной шаблон диалога приложения.
    Отображается в центре окна.
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow):

        # первоначальные настройки
        Popup.__init__(self, object_name, window)

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


class Message(Popup):

    """
    Popup message that dissapears on user click /
    Всплывающее сообщение, исчезающее по щелчку.
    """

    def __init__(
            self,
            object_name: str,
            window: dynamic.DynamicWindow,
            previous: QtWidgets.QDialog = None):

        Popup.__init__(self, object_name, window, previous)
        self.sea.clicked.connect(lambda e: self.close())

    def show_(self, geo: QtCore.QRect):
        self.island.setGeometry(geo)
        self.show()
