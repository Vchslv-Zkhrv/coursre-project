import time
import math

from PyQt6 import QtCore, QtGui, QtWidgets

from . import dynamic
from . import shorts
from .dynamic import global_widget_manager as gwm
from . import widgets
from . import gui
from . import config as cfg


class Floating(dynamic.DynamicDialog):

    island: dynamic.DynamicButton
    label: dynamic.DynamicLabel

    def __init__(self, window: dynamic.DynamicWindow):

        dynamic.DynamicDialog.__init__(self)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool)
        layout = shorts.GLayout(self)

        self.island = dynamic.DynamicButton()
        self.island.dont_translate = True
        layout.addWidget(self.island)
        self.island.setContentsMargins(cfg.GAP, cfg.GAP, cfg.GAP, cfg.GAP)
        self.island.signals.triggered.connect(
            lambda trigger: self._island_triggered(trigger)
        )
        gwm.add_widget(self.island)
        gwm.set_style(
            self.island,
            "always",
            f"""
                border-radius: {cfg.radius()}px;
                border: none;
                outline: none;
                padding: {cfg.GAP}px;
            """
        )
        gwm.set_style(
            self.island,
            "leave",
            """
                background-color: !highlight2!;
                color: !fore!;
            """
        )
        self.island.setStyleSheet("background-color: none")
        self.island.setMinimumHeight(cfg.radius()*2)
        self.window_ = window

        effect = QtWidgets.QGraphicsOpacityEffect(self.island)
        self.island.setGraphicsEffect(effect)
        self.animation = QtCore.QPropertyAnimation(effect, b"opacity")
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setDuration(150)

    def show(self):
        super().show()
        self.animation.start()

    def show_(self, text: str):
        print("show_")
        self.setText(text)
        pos = self.window_.cursor().pos()
        x = pos.x() - int(self.island.width() / 2)
        y = pos.y() - int(self.island.height() / 2)
        self.move(x+cfg.GAP*2, y+cfg.GAP*2)
        self.show()

    def _island_triggered(self, trigger: dynamic.widget_trigger):
        if trigger == "leave":
            self.reject()

    def setText(self, text: str):

        if len(text) > 500:
            text = text[:500] + "..."

        if len(text) > 100:
            lines = []
            for i in range(math.ceil(len(text)/100)):
                lines.append(text[i*100:(i+1)*100])
            text = "\n".join(lines)

        return self.island.setText(text)

    def text(self) -> str:
        return self.island.text()
