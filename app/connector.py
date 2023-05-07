import os
from sqlite3 import Connection

from loguru import logger

"""
Module working with external data sources /
Модуль, отвечающий за работу со внешними данными
"""


class EmptySet(Exception):

    """
    SQL exception for empty SELECT responses. /
    SQL - исключение для пустых ответов на SELECT запросы.
    """


class SQL(Connection):

    """
    Main sqlite connector. /
    Главный sqlite-коннектор.
    """

    def __init__(self, path: str):
        if os.path.exists(path):
            logger.debug(f"Connecting: {path}")
        else:
            logger.debug(f"Creating: {path}")
        Connection.__init__(self, path, check_same_thread=False)
        self._cursor = self.cursor()

    def exec(self, query: str) -> list:
        # приведение запроса в нормальный вид
        query = " ".join(query.split(" "))
        query = query.replace("  ", " ")
        # трассировка
        logger.info(query)
        # выполнение
        response = self._cursor.execute(query).fetchall()
        # коммит если необходимо
        command = query.split(" ")[0].lower()
        if command in ("insert", "update", "delete", "alter"):
            self.commit()
        # возвращение результата
        return response

    def select(self, query: str) -> list:
        response = self.exec(query)
        if not response: 
            raise EmptySet()
        else:
            logger.error("empty set")
            return response
