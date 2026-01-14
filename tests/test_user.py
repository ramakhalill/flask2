import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.controllers.userController as controller
from app.controllers.userController import (
    create_user,
    update_user,
    delete_user,
    get_user_book_count,
)
from app.extensions import db


# ------------------------------------

class FakeUser:
    def __init__(self, name="Old User"):
        self.id = 1
        self.name = name
        self.library = None


class FakeLibrary:
    def __init__(self, id=1):
        self.id = id


class FakeBookQuery:
    def __init__(self, count_value):
        self._count = count_value

    def filter_by(self, **kwargs):
        return self

    def count(self):
        return self._count


class FakeSession:
    def add(self, obj):
        pass

    def delete(self, obj):
        pass

    def commit(self):
        pass


# -----------------------------------

def test_create_user_success(monkeypatch):
    monkeypatch.setattr(db, "session", FakeSession())

    data = {"name": "Mock User"}

    user, error = create_user(data)

    assert error is None
    assert user.name == "Mock User"


def test_create_user_without_name():
    data = {}

    user, error = create_user(data)

    assert user is None
    assert error == "name is required"


# ----------------------------------

def test_update_user_success(monkeypatch):
    fake_user = FakeUser()

    class FakeUserQuery:
        def get(self, id):
            return fake_user

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    user, error = update_user(1, {"name": "New Name"})

    assert error is None
    assert user.name == "New Name"


def test_update_user_not_found(monkeypatch):
    class FakeUserQuery:
        def get(self, id):
            return None

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    user, error = update_user(99, {"name": "X"})

    assert user is None
    assert error == "user not found"


# ------------------------------

def test_delete_user_success(monkeypatch):
    fake_user = FakeUser()

    class FakeUserQuery:
        def get(self, id):
            return fake_user

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    success, error = delete_user(1)

    assert success is True
    assert error is None


def test_delete_user_not_found(monkeypatch):
    class FakeUserQuery:
        def get(self, id):
            return None

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    success, error = delete_user(99)

    assert success is False
    assert error == "user not found"


# -------------------------------

def test_get_user_book_count_success(monkeypatch):
    fake_user = FakeUser()
    fake_user.library = FakeLibrary(id=1)

    class FakeUserQuery:
        def get(self, id):
            return fake_user

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    monkeypatch.setattr(
        controller,
        "Book",
        type("FakeBook", (), {"query": FakeBookQuery(3)})
    )

    count, error = get_user_book_count(1)

    assert error is None
    assert count == 3


def test_get_user_book_count_no_library(monkeypatch):
    fake_user = FakeUser()
    fake_user.library = None

    class FakeUserQuery:
        def get(self, id):
            return fake_user

    monkeypatch.setattr(controller, "User", FakeUser)
    FakeUser.query = FakeUserQuery()

    count, error = get_user_book_count(1)

    assert count is None
    assert error == "user or library not found"
