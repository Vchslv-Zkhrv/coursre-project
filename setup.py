import os

from loguru import logger

from app import application
"""
Запуск приложения
"""

logger.add(
    f"{os.getcwd()}\\logs\\debug.log",
    rotation="1MB")

logger.debug("application start")
application.Application()
logger.debug("application finish")
