"""Модуль, описывающий взаимодействие с БД SQLite3"""

from typing import Any
from inspect import get_annotations
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """Класс, реализующий хранение данных в SQLite3"""
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                q = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(q)
        con.close()

    def add(self, obj: T) -> int:
        """Добавление обьекта в БД"""
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'Try to add object {obj} with filled `pk` attribute')

        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            q = f'INSERT INTO {self.table_name} ({names}) VALUES ({p})'
            cur.execute(q, values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def __generate_object(self, db_row: tuple) -> T:
        """ Преобразование данных из БД в обьект"""
        obj = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            row = cur.execute(q).fetchone()
        con.close()

        if row is None:
            return None

        return self.__generate_object(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            if where is not None:
                update_q = " AND ".join([f"{field} = ?" for field in where.keys()])
                rows = cur.execute(f'SELECT * FROM {self.table_name} WHERE {update_q}', list(where.values())).fetchall()
            else:
                rows = cur.execute(f'SELECT * FROM {self.table_name}').fetchall()

        con.close()

        if not rows:
            return None

        return [self.__generate_object(row) for row in rows]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте в БД"""
        if getattr(obj, 'pk', None) is None:
            raise ValueError('Try to update object without `pk` attribute')

        values = [getattr(obj, x) for x in self.fields]
        values.append(obj.pk)
        fields = ", ".join([f"{field}=?" for field in self.fields.keys()])

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'UPDATE {self.table_name} SET {fields} WHERE pk = ?', values)

            if cur.rowcount == 0:
                raise ValueError('attempt to update object with unknown primary key')

        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')

            if cur.rowcount == 0:
                raise ValueError('attempt to delete object with unknown primary key')
        con.close()
