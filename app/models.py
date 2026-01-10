from datetime import datetime
from .extensions import db

class Library(db.Model): #table
    __tablename__ = "libraries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # one library -> many books
    books = db.relationship(
        "Book",
        backref="library",
        cascade="all, delete-orphan",
        lazy=True
    )

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)

    library_id = db.Column(db.Integer, db.ForeignKey("libraries.id"), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
