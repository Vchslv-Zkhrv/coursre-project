import os
import sys

from loguru import logger

from app import application

"""
Application entry point /
Запуск приложения
"""

# настройка логирования
logger.add(
    f"{os.getcwd()}\\logs\\debug.log",
    rotation="1MB")

# первая запись в логи
logger.debug("START")

# создание и запуск приложения
app = application.Application(sys.argv)
exit_code = app.run()

# последняя запись в логи
if exit_code == 0:
    logger.debug("FINISH")
else:
    logger.critical(f"FINISH with exit code = {exit_code}")

sys.exit(exit_code)
