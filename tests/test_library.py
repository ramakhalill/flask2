import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.controllers.libraryController as controller
from app.controllers.libraryController import (
    create_library,
    update_library,
    delete_library,
)
from app.extensions import db


# ------------------------------------

class FakeLibrary:
    def __init__(self, name="Old Name"):
        self.id = 1
        self.name = name


class FakeSession:
    def add(self, obj):
        pass

    def delete(self, obj):
        pass

    def commit(self):
        pass


# ------------------------------------

def test_create_library_with_mock(monkeypatch):
    monkeypatch.setattr(db, "session", FakeSession())

    data = {"name": "Mock Library"}

    library, error = create_library(data)

    assert error is None
    assert library.name == "Mock Library"


def test_create_library_without_name_mock():
    data = {}

    library, error = create_library(data)

    assert library is None
    assert error == "name is required"


# ------------------------------------

def test_update_library_mock(monkeypatch):
    fake_library = FakeLibrary()

    class FakeQuery:
        def get(self, id):
            return fake_library

    monkeypatch.setattr(controller, "Library", FakeLibrary)
    FakeLibrary.query = FakeQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    lib, error = update_library(1, {"name": "New Name"})

    assert error is None
    assert lib.name == "New Name"


# -----------------------------------

def test_delete_library_success(monkeypatch):
    fake_library = FakeLibrary()

    class FakeQuery:
        def get(self, id):
            if id == fake_library.id:
                return fake_library
            return None

    monkeypatch.setattr(controller, "Library", FakeLibrary)
    FakeLibrary.query = FakeQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    success, error = delete_library(1)

    assert success is True
    assert error is None


def test_delete_library_not_found(monkeypatch):
    class FakeQuery:
        def get(self, id):
            return None

    monkeypatch.setattr(controller, "Library", FakeLibrary)
    FakeLibrary.query = FakeQuery()

    success, error = delete_library(99)

    assert success is False
    assert error == "library not found"
