from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
import sqlite3
import pytest


@pytest.fixture
def drop_table():
    with sqlite3.connect("test.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS custom;")


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        category: int = 0
        comment: str = 'a'
        expense_datetime: str = ''
        added_date: str = ''
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class, drop_table):
    return SQLiteRepository(db_file="test.db", cls=custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_update_unexistent(repo, custom_class):
    obj = custom_class()
    obj.pk = 2
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_without_pk(repo, custom_class):
    with pytest.raises(ValueError):
        repo.update(0)


def test_get_unexistent(repo):
    assert repo.get(-1) is None


def test_cannot_delete_unexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(-1)


def test_get_all(repo, custom_class):
    objs = [custom_class() for i in range(5)]
    for obj in objs:
        repo.add(obj)
    assert repo.get_all() == objs


def test_get_all_with_condition(repo, custom_class):
    objs = []
    for i in range(5):
        obj = custom_class(category=i)
        repo.add(obj)
        objs.append(obj)
    res = repo.get_all({'category': 0})
    assert res == [objs[0]]
    assert repo.get_all({'comment': 'a'}) == objs
