import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.controllers.bookController as controller
from app.controllers.bookController import (
    create_book,
    update_book,
    delete_book,
    transfer_book,
)
from app.extensions import db


# ------------------------------------

class FakeBook:
    def __init__(self, title="Old Title", author="Old Author", library_id=1):
        self.id = 1
        self.title = title
        self.author = author
        self.library_id = library_id


class FakeLibrary:
    def __init__(self, id=1):
        self.id = id


class FakeSession:
    def add(self, obj):
        pass

    def delete(self, obj):
        pass

    def commit(self):
        pass


# ------------------------------------

def test_create_book_success(monkeypatch):
    class FakeLibraryQuery:
        def get(self, id):
            return FakeLibrary(id)

    monkeypatch.setattr(controller, "Library", FakeLibrary)
    FakeLibrary.query = FakeLibraryQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    data = {
        "title": "Mock Book",
        "author": "Mock Author",
        "library_id": 1,
    }

    book, error = create_book(data)

    assert error is None
    assert book.title == "Mock Book"
    assert book.author == "Mock Author"


def test_create_book_missing_data():
    data = {}

    book, error = create_book(data)

    assert book is None
    assert error == "all the fields are required!"


# ------------------------------------

def test_update_book_success(monkeypatch):
    fake_book = FakeBook()

    class FakeBookQuery:
        def get(self, id):
            return fake_book

    class FakeLibraryQuery:
        def get(self, id):
            return FakeLibrary(id)

    monkeypatch.setattr(controller, "Book", FakeBook)
    monkeypatch.setattr(controller, "Library", FakeLibrary)

    FakeBook.query = FakeBookQuery()
    FakeLibrary.query = FakeLibraryQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    book, error = update_book(1, {"title": "New Title"})

    assert error is None
    assert book.title == "New Title"


# ------------------------------------

def test_delete_book_success(monkeypatch):
    fake_book = FakeBook()

    class FakeBookQuery:
        def get(self, id):
            return fake_book

    monkeypatch.setattr(controller, "Book", FakeBook)
    FakeBook.query = FakeBookQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    success, error = delete_book(1)

    assert success is True
    assert error is None


def test_delete_book_not_found(monkeypatch):
    class FakeBookQuery:
        def get(self, id):
            return None

    monkeypatch.setattr(controller, "Book", FakeBook)
    FakeBook.query = FakeBookQuery()

    success, error = delete_book(99)

    assert success is False
    assert error == "book not found"


# ------------------------------------

def test_transfer_book_success(monkeypatch):
    fake_book = FakeBook(library_id=1)

    class FakeBookQuery:
        def get(self, id):
            return fake_book

    class FakeLibraryQuery:
        def get(self, id):
            return FakeLibrary(id)

    monkeypatch.setattr(controller, "Book", FakeBook)
    monkeypatch.setattr(controller, "Library", FakeLibrary)

    FakeBook.query = FakeBookQuery()
    FakeLibrary.query = FakeLibraryQuery()

    monkeypatch.setattr(db, "session", FakeSession())

    book, error = transfer_book(1, 2)

    assert error is None
    assert book.library_id == 2


def test_transfer_book_library_not_found(monkeypatch):
    fake_book = FakeBook()

    class FakeBookQuery:
        def get(self, id):
            return fake_book

    class FakeLibraryQuery:
        def get(self, id):
            return None

    monkeypatch.setattr(controller, "Book", FakeBook)
    monkeypatch.setattr(controller, "Library", FakeLibrary)

    FakeBook.query = FakeBookQuery()
    FakeLibrary.query = FakeLibraryQuery()

    book, error = transfer_book(1, 99)

    assert book is None
    assert error == "destination library not found"
