from PyQt6 import QtWidgets
"""
Module with modified PyQt6 basic widgets /
Модуль с модифицированными виджетами PyQt6.

There are ready-made widgets that may be created with one line of code /
Готовые виджеты, создаваемые одной строкой кода

"""


class VSpacer(QtWidgets.QSpacerItem):
    def __init__(self, height: int = 0):
        QtWidgets.QSpacerItem.__init__(
            self,
            0,
            height,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding)


class HSpacer(QtWidgets.QSpacerItem):
    def __init__(self, width: int = 0):
        QtWidgets.QSpacerItem.__init__(
            self,
            width,
            0,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum)


class HLayout(QtWidgets.QHBoxLayout):
    def __init__(self, parent):
        QtWidgets.QHBoxLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class VLayout(QtWidgets.QVBoxLayout):
    def __init__(self, parent):
        QtWidgets.QHBoxLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class GLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        QtWidgets.QGridLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class ExpandingPolicy(QtWidgets.QSizePolicy):
    def __init__(self):
        QtWidgets.QSizePolicy.__init__(
            self,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding)
        self.setHorizontalStretch(0)
        self.setVerticalStretch(0)


class FixedPolicy(QtWidgets.QSizePolicy):
    def __init__(self):
        QtWidgets.QSizePolicy.__init__(
            self,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed)
        self.setHorizontalStretch(0)
        self.setVerticalStretch(0)


class MinimumPolicy(QtWidgets.QSizePolicy):
    def __init__(self):
        QtWidgets.QSizePolicy.__init__(
            self,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum)
        self.setHorizontalStretch(0)
        self.setVerticalStretch(0)
