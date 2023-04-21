from PyQt6 import QtWidgets, QtCore, QtGui

from . import qt_shortcuts as shorts
from .config import CURRENT_THEME as THEME
"""
File with custom window template
"""


class WindowShadow(QtWidgets.QMainWindow):

    """
    translucent rectangle showing window target geometry /
    полупрозрачный прямоугольник, отображающий будущее расположение окна
    """

    def __init__(self, rect: QtCore.QRect):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(rect)
        self.setCentralWidget(QtWidgets.QWidget())
        r, g, b, a = THEME['fore'].getRgb()
        self.centralWidget().setStyleSheet(
            f"background-color: rgba({r}, {g}, {b}, 0.5); border:none;")

class WindowEdgeShadow(WindowShadow):
    
    """
    WindowShadow creating when user drags window to the screen edge/
    WindowShadow, создающийся когда пользователь перемещает окно в край монитора
    """

    def __init__(self, screen: QtGui.QScreen, edge: QtCore.Qt.Edge):
        geo = screen.geometry()
        if edge == QtCore.Qt.Edge.BottomEdge:
            raise AttributeError("bottom edge doesn't supported")
        if edge == QtCore.Qt.Edge.TopEdge:
            pass
        if edge == QtCore.Qt.Edge.LeftEdge:
            geo.setWidth(int(geo.width()/2))
        if edge == QtCore.Qt.Edge.RightEdge:
            w = int(geo.width()/2)
            geo.setX(w)
            geo.setWidth(w)
        WindowShadow.__init__(self, geo)


class TitleBar(QtWidgets.QFrame):

    """
    Custom window title bar. Provides window moving /
    Заголовок окна. Обеспечивает его перемещение.
    """

    def __init__(
            self,
            parent: QtWidgets.QMainWindow,
            height: int):

        QtWidgets.QFrame.__init__(self, parent)
        self.setFixedHeight(height)
        self.setSizePolicy(shorts.RowPolicy())

        self._is_pressed = False
        self._press_pos = None
        self._shadow: WindowShadow = None

    def get_event_absolute_pos(self, a0: QtGui.QMouseEvent) -> QtCore.QPoint:
        pos = a0.pos()
        x, y = pos.x(), pos.y()
        opos = self.window().pos()
        x += opos.x()
        y += opos.y()
        return QtCore.QPoint(x, y)

    def get_event_edge(self, a0: QtGui.QMouseEvent) -> QtCore.Qt.Edge | None:
        pos = self.get_event_absolute_pos(a0)
        x, y = pos.x(), pos.y()
        geo = self.screen().geometry()
        top, left, right, bottom = 0, 0, geo.right()-30, geo.bottom()-30
        if x < left:
            return QtCore.Qt.Edge.LeftEdge
        elif x > right:
            return QtCore.Qt.Edge.RightEdge
        elif y < top:
            return QtCore.Qt.Edge.TopEdge
        elif y > bottom:
            return QtCore.Qt.Edge.BottomEdge
        else:
            return None

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self._is_pressed = True
        self._press_pos = self.get_event_absolute_pos(a0)
        self.window().setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)
        print(f"pressed at {self._press_pos.x()} {self._press_pos.y()}")
        return super().mousePressEvent(a0)

    def _show_shadow(self, edge: QtCore.Qt.Edge):
        if edge == None and self._shadow:
            self._shadow.close()
            self._shadow = None
            return
        if edge == QtCore.Qt.Edge.BottomEdge and self._shadow:
            self._shadow.close()
            self._shadow = None
            return
        if edge == QtCore.Qt.Edge.BottomEdge and not self._shadow:
            return
        if edge and not self._shadow:
            self._shadow = WindowEdgeShadow(self.screen(), edge)
            self._shadow.show()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        edge = self.get_event_edge(a0)
        self._show_shadow(edge)
        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self._shadow:
            self._shadow.close()
            self._shadow = None
        self.window().setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        if self._is_pressed:
            pos1 = self.get_event_absolute_pos(a0)
            print(f"realesed at {pos1.x()} {pos1.y()}")
            pos0 = self._press_pos
            dx = pos1.x() - pos0.x()
            dy = pos1.y() - pos0.y()
            opos = self.window().pos()
            self.window().move(dx + opos.x(), dy + opos.y())
        self._is_pressed = False
        self._start_pos = None
        return super().mouseReleaseEvent(a0)


class SideGrip(QtWidgets.QWidget):

    def __init__(
            self,
            parent: QtWidgets.QMainWindow,
            edge: QtCore.Qt.Edge):

        QtWidgets.QWidget.__init__(self, parent)

        if edge == QtCore.Qt.Edge.LeftEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resize_func = self.resize_left
        elif edge == QtCore.Qt.Edge.TopEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resize_func = self.resize_top
        elif edge == QtCore.Qt.Edge.RightEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resize_func = self.resize_right
        else:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resize_func = self.resize_bottom

        self.mouse_pos = None

    def resize_left(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resize_top(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resize_right(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resize_bottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            delta = event.pos() - self.mouse_pos
            self.resize_func(delta)

    def mouseReleaseEvent(self, event):
        self.mouse_pos = None


class Window(QtWidgets.QMainWindow):

    """
    Framless window with re-implemented title bar /
    Окно без рамок
    """

    _grip_size = 8
    _titlebar_height = 44

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)


        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setCentralWidget(QtWidgets.QWidget())
        layout = shorts.VLayout(self.centralWidget())

        self.title_bar = TitleBar(self, self._titlebar_height)
        layout.addWidget(self.title_bar)

        self.content = QtWidgets.QFrame(self)
        self.content.setSizePolicy(shorts.ExpandingPolicy())
        layout.addWidget(self.content)

        self.title_bar.setStyleSheet("border: 1px solid rgb(14,14,14);")

        self.side_grips = [
            SideGrip(self, QtCore.Qt.Edge.LeftEdge),
            SideGrip(self, QtCore.Qt.Edge.TopEdge),
            SideGrip(self, QtCore.Qt.Edge.RightEdge),
            SideGrip(self, QtCore.Qt.Edge.BottomEdge),
        ]
        self.corner_grips = [QtWidgets.QSizeGrip(self) for i in range(4)]

    def setStyleSheet(self, styleSheet: str) -> None:
        self.centralWidget().setStyleSheet(styleSheet)
        return super().setStyleSheet(styleSheet)

    @property
    def grip_size(self):
        return self._grip_size

    def set_grip_size(self, size):
        if size == self._grip_size:
            return
        self._grip_size = max(2, size)
        self.update_grips()

    def update_grips(self):

        self.setContentsMargins(*[self.grip_size] * 4)
        out_rect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        in_rect = out_rect.adjusted(
            self.grip_size,
            self.grip_size,
            -self.grip_size,
            -self.grip_size)

        # top left
        self.corner_grips[0].setGeometry(
            QtCore.QRect(out_rect.topLeft(), in_rect.topLeft()))

        # top right
        self.corner_grips[1].setGeometry(
            QtCore.QRect(out_rect.topRight(), in_rect.topRight()).normalized())

        # bottom right
        self.corner_grips[2].setGeometry(
            QtCore.QRect(in_rect.bottomRight(), out_rect.bottomRight()))

        # bottom left
        self.corner_grips[3].setGeometry(
            QtCore.QRect(out_rect.bottomLeft(), in_rect.bottomLeft()).normalized())

        # left edge
        self.side_grips[0].setGeometry(
            0, in_rect.top(), self.grip_size, in_rect.height())

        # top edge
        self.side_grips[1].setGeometry(
            in_rect.left(), 0, in_rect.width(), self.grip_size)

        # right edge
        self.side_grips[2].setGeometry(
            in_rect.left() + in_rect.width(),
            in_rect.top(),
            self.grip_size,
            in_rect.height())

        # bottom edge
        self.side_grips[3].setGeometry(
            self.grip_size,
            in_rect.top() + in_rect.height(),
            in_rect.width(),
            self.grip_size)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.update_grips()
