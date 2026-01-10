from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from .extensions import db
from .models import Library, Book

api = Blueprint("api", __name__)

def library_to_dict(lib: Library):
    return {"id": lib.id, "name": lib.name}

def book_to_dict(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "library_id": book.library_id,
        "created_at": book.created_at.isoformat()
    }

def get_json():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {} #so if its garbage data dont get the server down 

@api.post("/libraries")
def create_library():
    data = get_json()
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required!!"}), 400

    lib = Library(name=name)
    db.session.add(lib)
    db.session.commit()
    return jsonify(library_to_dict(lib)), 201

@api.get("/libraries")
def list_libraries():
    libs = Library.query.order_by(Library.id.asc()).all()
    return jsonify([library_to_dict(l) for l in libs])

@api.patch("/libraries/<int:library_id>")
def update_library(library_id: int):
    lib = Library.query.get_or_404(library_id)
    data = get_json()
    name = data.get("name")
    if name is not None:
        name = name.strip()
        if not name:
            return jsonify({"error": "the name cantt be empty"}), 400
        lib.name = name
    db.session.commit()
    return jsonify(library_to_dict(lib))

@api.delete("/libraries/<int:library_id>")
def delete_library(library_id: int):
    lib = Library.query.get_or_404(library_id)
    db.session.delete(lib)
    db.session.commit()
    return jsonify({"message": "library deleted"})


@api.post("/books")
def create_book():
    data = get_json()
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    library_id = data.get("library_id")

    if not title or not author or not library_id:
        return jsonify({"error": "title, author, and library_id are required"}), 400

    lib = Library.query.get(library_id)
    if not lib:
        return jsonify({"error": "library_id does not exist"}), 400

    book = Book(title=title, author=author, library_id=library_id)
    db.session.add(book)
    db.session.commit()
    return jsonify(book_to_dict(book)), 201

@api.get("/books")
def list_books():
    library_id = request.args.get("library_id", type=int)
    q = (request.args.get("q") or "").strip()

    query = Book.query

    books = query.order_by(Book.created_at.desc()).all()
    return jsonify([book_to_dict(b) for b in books])

@api.patch("/books/<int:book_id>")
def update_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    data = get_json()

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        book.title = title

    if "author" in data:
        author = (data.get("author") or "").strip()
        if not author:
            return jsonify({"error": "author cannot be empty"}), 400
        book.author = author

    if "library_id" in data:
        new_library_id = data.get("library_id")
        if not new_library_id:
            return jsonify({"error": "library_id cannot be empty"}), 400
        if not Library.query.get(new_library_id):
            return jsonify({"error": "library_id does not exist"}), 400
        book.library_id = new_library_id

    db.session.commit()
    return jsonify(book_to_dict(book))

@api.delete("/books/<int:book_id>")
def delete_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "book deleted"})

