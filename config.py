import os
import sys
from dataclasses import dataclass
from abc import abstractmethod
from typing import Literal, TypedDict, NewType
from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore, QtSvg
from loguru import logger

