from typing import Literal

from PyQt6 import QtWidgets, QtCore, QtGui

"""
File with custom window template
"""


class Window(QtWidgets.QMainWindow):

    """custom window with no border"""

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
