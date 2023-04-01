import os

from loguru import logger

from app import application

"""
Запуск приложения
"""

logger.add(
    f"{os.getcwd()}\\logs\\debug.log",
    level="INFO",
    rotation="1MB")

application.Application()
