import time
import math
import threading

from PyQt6 import QtCore, QtWidgets

from . import dynamic
from . import shorts
from .dynamic import global_widget_manager as gwm
from . import config as cfg


class Timer(QtCore.QObject):

    finished = QtCore.pyqtSignal()

    def run(self, delay: float):
        threading.Thread(target=self.wait, args=(delay, )).start()

    def wait(self, delay: float):
        time.sleep(delay)
        self.finished.emit()


class Floating(dynamic.DynamicDialog):

    island: dynamic.DynamicButton
    label: dynamic.DynamicLabel
    thread_: QtCore.QThread
    waiting: str

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

        self.waiting = ""

    def dont_show(self):
        self.waiting = ""

    def _show_later(self):
        if self.waiting:
            print("I'll show")
            self.show_(self.waiting)
        else:
            print("drop waiting")

    def show_later(self, text: str, delay: float):
        timer = Timer()
        self.waiting = text
        timer.finished.connect(self._show_later)
        timer.run(delay)

    def retire(self):

        if not self.geometry().contains(self.window_.cursor().pos()):
            self.hide()

    def show(self):
        super().show()
        self._opacity_animation(0, 1)

    def show_(self, text: str, ttl: float = 3):
        self.setText(text)
        self.place(self.window_.cursor().pos())
        self.show()
        self._set_kill_timer(ttl)

    def place(self, anchor: QtCore.QPoint):
        x = anchor.x() - 2
        y = anchor.y() - 2
        self.move(x, y)
        geo = self.geometry()
        if geo.right() > self.window_.width() - cfg.GAP:
            self.move(
                self.window_.x() + self.window_.width() - self.width() - cfg.GAP,
                self.y()
            )
        if geo.bottom() > self.window_.height() - cfg.GAP:
            self.move(
                self.x(),
                self.window_.y() + self.window_.height() - self.height() - cfg.GAP
            )

    def _opacity_animation(self, start: float, end: float):
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def _set_kill_timer(self, ttl: float):
        timer = Timer()
        timer.finished.connect(self.retire)
        timer.run(ttl)

    def _island_triggered(self, trigger: dynamic.widget_trigger):
        if trigger == "leave":
            self.hide()

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
