import os

from PyQt6 import QtGui, QtWidgets

from . import config as cfg


class Font(QtGui.QFont):

    """
    Base font object /
    Базовый объект шрифта
    """

    def __init__(self, path: str, size: int, weight: int = None):
        id_ = QtGui.QFontDatabase.addApplicationFont(path)
        families = QtGui.QFontDatabase.applicationFontFamilies(id_)
        QtGui.QFont.__init__(self, families[0])
        self.setPixelSize(size)
        if weight:
            self.setWeight(weight)


class FontFamily():

    """
    Fonts factory /
    Фабрика шрифтов
    """

    def __init__(self, name: str, size: int = 14, style: str = "Regular", weight: int = None):
        self.size = size
        self.weight = weight
        self.style = style
        self.path = f"{os.getcwd()}{cfg.FONTS_PATH}\\{name}\\%s.ttf"

    def font(self,
             size: int = None,
             style: str = None,
             weight: int = None):

        size = size if size else self.size
        weight = weight if weight else self.weight
        style = style if style else self.style
        return Font(self.path % style, size, weight)


main_family = FontFamily(cfg.MAIN_FONT_FAMILY, style="Light")
head_family = FontFamily(cfg.HEAD_FONT_FAMILY, 20)
mono_family = FontFamily(cfg.MONO_FONT_FAMILY)
