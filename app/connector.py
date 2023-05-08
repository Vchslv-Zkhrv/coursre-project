import os
from sqlite3 import Connection, Cursor
from dataclasses import dataclass

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


@dataclass
class Column():

    name: str
    type_: type

    is_pk: bool = False
    is_fk: bool = False
    is_unique: bool = False
    is_calculated: bool = False
    is_not_null: bool = False


@dataclass
class Table():

    name: str
    lenght: str
    columns: tuple[Column]


class SQL(Connection):

    """
    Main sqlite connector. /
    Главный sqlite-коннектор.
    """

    tables: dict[str, Table]

    def __init__(self, path: str):
        if os.path.exists(path):
            logger.debug(f"Connecting: {path}")
        else:
            logger.debug(f"Creating: {path}")
        Connection.__init__(self, path, check_same_thread=False)
        self._cursor = self.cursor()
        self.tables = self._parse_database()

    def exec(self, query: str) -> Cursor:
        # приведение запроса в нормальный вид
        query = " ".join(query.split(" "))
        query = query.replace("  ", " ")
        # трассировка
        logger.info(query)
        # выполнение
        response = self._cursor.execute(query)
        # коммит если необходимо
        command = query.split(" ")[0].lower()
        if command in ("insert", "update", "delete", "alter"):
            self.commit()
        # возвращение результата
        return response

    def select(self, query: str) -> list:
        """
        Executes query and returns response (or raises EmptySet exceprtion) /
        Выполняет запрос и возвращает ответ (или вызывает исключение EmptySet)
        """
        response = self.exec(query).fetchall()
        if not response:
            raise EmptySet()
        else:
            logger.error("empty set")
            return response

    def _parse_database(self) -> dict[str, Table]:
        tables = dict()
        tablenames = self._get_tablenames()
        for tablename in tablenames:
            lenght = self._get_table_lenght(tablename)
            columnnames = self._get_column_names(tablename)
            columns = []
            for columnname in columnnames:
                type_ = self._get_column_type(tablename, columnname)
                columns.append(Column(
                    columnname,
                    type_))
            tables[tablename] = Table(tablename, lenght, tuple(columns))
        return tables

    def _get_column_type(self, tablename: str, columnname: str) -> type:
        response = self.select(f"SELECT {columnname} FROM {tablename} LIMIT 1")[0][0]
        return type(response)

    def _get_tablenames(self) -> tuple[str]:
        tablenames = self.select("SELECT name FROM sqlite_schema WHERE type = \"table\"")
        tablenames = sorted(list((row[0] for row in tablenames)))
        if "sqlite_sequence" in tablenames:
            tablenames.remove("sqlite_sequence")
        return tuple(tablenames)

    def _get_table_lenght(self, tablename: str) -> int:
        return self.select(f"SELECT count(*) FROM {tablename}")[0][0]

    def _get_column_names(self, tablename: str) -> tuple[str]:
        # sqlite не позволяет получить имена столбцов,
        # однако можно получить полный текст команды CREATE TABLE
        query = f"SELECT sql FROM sqlite_schema WHERE name='{tablename}'"
        # текст команды в исходном виде
        sql = self.select(query)[0][0].strip()[:-2]
        # заменяем переносы строки на пробел
        sql = " ".join(sql.split("\n"))
        # отсекаем CREATE TABLE ... ( и разбиваем на столбцы по запятой
        columns = sql.split("(")[1].split(",")
        # избавлемся от висячих пробелов
        names = tuple(col.split()[0].strip() for col in columns)
        # удаляем Foregin key и primary keн
        names = tuple(filter(lambda name: "FOREIGN" not in name.upper(), names))
        names = tuple(filter(lambda name: "PRIMARY" not in name.upper(), names))
        return names
