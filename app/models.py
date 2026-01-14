from datetime import datetime
from .extensions import db


class Library(db.Model): #table
    __tablename__ = "libraries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    #one to many relation
    books = db.relationship(
        "Book",
        backref="library",
        cascade="all, delete-orphan",
        lazy=True
    )


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(25), nullable=False)

    library_id = db.Column(db.Integer, db.ForeignKey("libraries.id"), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    # one to one 
    library = db.relationship(
        "Library",
        backref="owner",
        uselist=False,
        cascade="all, delete-orphan"
    )