from PyQt6 import QtWidgets

from .window import AbstractWindow
from .cwindow import modes

class AuthorizationForm(AbstractWindow):

    """
    Authorization form showed when application launched /
    Форма авторизации, отображающаяся при запуске приложения
    """

    def __init__(self):

        AbstractWindow.__init__(self)
        self.gesture_mode = modes.GestureResizeModes.never
        self.setFixedSize(720, 480)