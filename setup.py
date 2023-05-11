import os
import sys

from loguru import logger

from app import application

"""
Запуск приложения
"""

logger.add(
    f"{os.getcwd()}\\logs\\debug.log",
    rotation="1MB")

logger.debug("START")

app = application.Application(sys.argv)
sys.exit(app.run())
