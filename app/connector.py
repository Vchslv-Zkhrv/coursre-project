import os
from hashlib import sha256
from typing import Any, Literal
from sqlite3 import Connection, Cursor
from dataclasses import dataclass

from loguru import logger

from . import config as cfg
from .actions import User

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
    default: Any | None = None

    is_pk: bool = False
    is_fk: bool = False
    is_not_null: bool = False
    is_unique: bool = False
    is_calculated: bool = False


class Table():

    name: str
    lenght: int
    columns: tuple[Column]

    def __init__(self, name: str, lenght: int, columns: tuple[Column]):
        self.name = name
        self.lenght = lenght
        self.columns = columns

    def column(self, columnname: str) -> Column:
        for col in self.columns:
            if col.name == columnname:
                return col


operand = Literal[">", "<", ">=", "<=", "=", "like", "is null", "is not null"]


class Where():

    """
    Where clause object for simple queries/
    объект конструкции Where для простых запросов
    """

    text: str

    column: Column
    operand_: operand
    value: Any

    def __init__(self, column: Column, operand_: operand, value: Any = None):
        self.column = column
        self.operand_ = operand_
        self.value = value
        self.text = self._generate_text()

    def _generate_text(self) -> str:
        if self.column.type_ == str:
            value = f"'{self.value}'"
        else:
            value = str(self.value)
        if self.value:
            return f"({self.column.name} {self.operand_} {value})"
        else:
            return f"({self.column.name} {self.operand_})"

    def __mul__(self, other) -> str:
        if isinstance(other, str):
            return f"{self.text} AND {other}"
        else:
            return f"{self.text} AND {other.text}"

    def __add__(self, other):
        if isinstance(other, str):
            return f"{self.text} OR {other}"
        else:
            return f"{self.text} OR {other.text}"

    def __str__(self):
        return self.text


class SQL(Connection):

    """
    Main sqlite connector. /
    Главный sqlite-коннектор.
    """

    tables: dict[str, Table]
    echo: bool = True

    def __init__(self, path: str):
        self.echo = False
        parse = False
        if os.path.exists(path):
            parse = True
            logger.debug(f"Connecting: {path}")
        else:
            logger.debug(f"Creating: {path}")
        Connection.__init__(self, path, check_same_thread=False)
        self._cursor = self.cursor()
        if parse:
            self.tables = self._parse_database()
        else:
            self.tables = ()
        self.exec("PRAGMA FOREIGN_KEYS = ON;")
        self.exec("PRAGMA SQLITE_ENABLE_MATH_FUNCTIONS = ON;")
        self.echo = True

    def update(self):
        self.echo = False
        self.tables = self._parse_database()
        self.echo = True

    def exec(self, query: str) -> Cursor:
        # приведение запроса в нормальный вид
        query = self._normilize_sql(query)
        # трассировка
        if self.echo:
            logger.info(query)
        # выполнение
        response = self._cursor.execute(query)
        # коммит если необходимо
        command = query.split(" ")[0].lower()
        if command in ("insert", "update", "delete", "alter"):
            self.commit()
        # возвращение результата
        return response

    def select(self, query: str) -> list[Any]:
        """
        Executes query and returns response (or raises EmptySet exceprtion) /
        Выполняет запрос и возвращает ответ (или вызывает исключение EmptySet)
        """
        response = self.exec(query).fetchall()
        if not response:
            if self.echo:
                logger.error("empty set")
            raise EmptySet()
        else:
            return response

    def _parse_database(self) -> dict[str, Table]:

        tables = dict()
        tablenames = self._get_tablenames()

        for tablename in tablenames:
            fks = self._get_table_fks(tablename)
            lenght = self._get_table_lenght(tablename)
            columnnames = self._get_column_names(tablename)
            columns = []

            for columnname in columnnames:
                type_ = self._get_column_type(tablename, columnname)
                default = self._get_column_default(tablename, columnname)
                is_pk, not_null, unique, calculated = self._get_column_constraints(
                    tablename, columnname)
                columns.append(Column(
                    columnname,
                    type_,
                    default,
                    is_pk,
                    columnname in fks,
                    not_null,
                    unique,
                    calculated))

            tables[tablename] = Table(tablename, lenght, tuple(columns))
        return tables

    def _get_table_fks(self, tablename: str) -> tuple[str]:
        sql = "(".join(self._get_table_sql(tablename).split("(")[1:])[:-1]
        columns = sql.split(",")
        fks = []
        while columns:
            column = self._normilize_sql(columns.pop()).lower()
            if column.startswith("foreign key"):
                fks.append(column.split("(")[1].split(")")[0].strip())
        return tuple(fks)

    def _get_column_constraints(
            self,
            tablename: str,
            columnname: str) -> tuple[bool, bool, bool, bool]:

        column_sql = self._get_column_sql(tablename, columnname).lower()
        return (
            "primary key" in column_sql,
            "not null" in column_sql,
            "unique" in column_sql,
            "generated" in column_sql
        )

    def _get_column_default(self, tablename: str, columnname: str) -> Any:
        sql = self._get_column_sql(tablename, columnname).lower()
        if "default" not in sql:
            return None
        else:
            type_ = self._get_column_type(tablename, columnname)
            return type_(sql.split("default ")[1].split(" ")[0])

    def _get_column_sql(self, tablename: str, columnname: str) -> str:
        sql = self._get_table_sql(tablename)
        columns = sql.split("(")[1].split(",")
        for column in columns:
            if columnname.lower() in column.lower():
                return self._normilize_sql(column)

    def _get_column_type(self, tablename: str, columnname: str) -> type:
        sql_type = self._get_column_sql(tablename, columnname).split(" ")[1].lower()
        return {
            "int": int,
            "integer": int,
            "real": float,
            "text": str,
            "blob": bytes,
            "tex": str
        }[sql_type]

    def _get_tablenames(self) -> tuple[str]:
        tablenames = self.select("SELECT name FROM sqlite_schema WHERE type = \"table\"")
        tablenames = sorted(list((row[0] for row in tablenames)))
        if "sqlite_sequence" in tablenames:
            tablenames.remove("sqlite_sequence")
        return tuple(tablenames)

    def _get_table_lenght(self, tablename: str) -> int:
        return self.select(f"SELECT count(*) FROM {tablename}")[0][0]

    def _normilize_sql(self, sql: str) -> str:
        sql = sql.strip()
        sql = " ".join(sql.split("\n"))
        while "  " in sql:
            sql = sql.replace("  ", " ")
        return sql

    def _get_table_sql(self, tablename: str) -> str:
        # sqlite не позволяет получить имена столбцов,
        # однако можно получить полный текст команды CREATE TABLE
        query = f"SELECT sql FROM sqlite_schema WHERE name='{tablename}'"
        # текст команды в исходном виде
        sql = self.select(query)[0][0].strip()[:-1]
        return self._normilize_sql(sql)

    def _get_column_names(self, tablename: str) -> tuple[str]:
        sql = self._get_table_sql(tablename)
        # отсекаем CREATE TABLE ... ( и разбиваем на столбцы по запятой
        columns = sql.split("(")[1].split(",")
        # избавлемся от висячих пробелов
        names = tuple(col.split()[0].strip() for col in columns)
        # удаляем Foregin key и primary keн
        names = tuple(filter(lambda name: "FOREIGN" not in name.upper(), names))
        names = tuple(filter(lambda name: "PRIMARY" not in name.upper(), names))
        return names

    def select_where(
            self,
            tablename: str,
            where: str,
            rowid: bool = False) -> tuple:

        target = "rowid, *" if rowid else "*"
        return self.select(f"SELECT {target} FROM {tablename} WHERE {where};")

    def get_rows(
            self,
            tablename: str,
            start: int,
            count: int,
            rowid: bool = False) -> tuple[tuple[Any]]:

        target = "rowid, *" if rowid else "*"
        start_ = start if start > 0 else self.tables[tablename].lenght-19
        start_ = start_ if start_ > 0 else start
        result = self.select(f"""
            SELECT {target}
            FROM {tablename}
            WHERE rowid >= {start_}
            LIMIT {count}""")
        if len(result) == count or start <= 1:
            return result
        else:
            print("recursion")
            return self.get_rows(
                tablename,
                start-1,
                count,
                rowid
            )


class ApplicationDatabase(SQL):

    def __init__(self):
        SQL.__init__(self, f"{os.getcwd()}\\{cfg.APP_DATABASE_PATH}")

    def log_in(self, login: str, password: str) -> User | None:
        if not login or not password:
            raise AttributeError("missing value")
        password = sha256(bytes(password, "utf-8")).hexdigest()
        lcolumn = self.tables["users"].column("login")
        pcolumn = self.tables["users"].column("password")
        where = Where(lcolumn, "=", login) * Where(pcolumn, "=", password)
        try:
            *_, group, last_proj = self.select_where("users", where)[0]
            return User(login, group, last_proj)
        except EmptySet:
            return None

    def _where_user(self, user: User) -> str:
        return f"login = '{user.login}'"

    def update_last_proj(self, user: User, path: str) -> None:
        self.exec(f"UPDATE users SET last_proj = '{path}' WHERE {self._where_user(user)}")
