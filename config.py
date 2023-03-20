import os
import sys
from dataclasses import dataclass
from abc import abstractmethod
from typing import Literal, TypedDict, NewType
from datetime import datetime
from sqlite3 import connect, OperationalError, IntegrityError, InternalError

from PyQt6 import QtWidgets, QtGui, QtCore, QtSvg
from loguru import logger



"""
Module containing imports, structures, global constants and state variables / 
Модуль, содержащий зависимости, структуры данных, глобальные константы и переменные состояния.

Must be imported by each module / Должен быть импортирован всеми остальными модулями.
"""

