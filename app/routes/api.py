from flask import Blueprint, request, jsonify
from ..models import Library, Book
from app.controllers.libraryController import create_library, update_library, delete_library
from app.controllers.bookController import create_book, transfer_book,update_book,delete_book,list_books
from app.http.httpstatus import HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND

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
def create_library_route():
    data = get_json()

    lib, error = create_library(data)

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify(library_to_dict(lib)), HTTP_201_CREATED


@api.get("/libraries")
def list_libraries():
    libs = Library.query.order_by(Library.id.asc()).all()
    return jsonify([library_to_dict(l) for l in libs])

@api.patch("/libraries/<int:library_id>")
def update_library_route(library_id):
    data = get_json()

    lib, error = update_library(library_id, data)

    if error:
        if error == "library not found":
            return jsonify({"error": error}), HTTP_404_NOT_FOUND
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify(library_to_dict(lib)), HTTP_200_OK 


@api.delete("/libraries/<int:library_id>")
def delete_library_route(library_id):
    success, error = delete_library(library_id)

    if error:
        return jsonify({"error": error}), HTTP_404_NOT_FOUND

    return jsonify({"message": "the library has been deleted successfully"}), 200


#-------------------------books-----------------------------

@api.post("/books")
def create_book_route():
    data = get_json()

    book, error = create_book(data)

    if error:
        if error == "library not found":
            return jsonify({"error": error}), HTTP_404_NOT_FOUND
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify(book_to_dict(book)), HTTP_201_CREATED


@api.get("/books")
def list_books():
    library_id = request.args.get("library_id", type=int)
    q = (request.args.get("q") or "").strip()

    query = Book.query

    books = query.order_by(Book.created_at.desc()).all()
    return jsonify([book_to_dict(b) for b in books])

@api.patch("/books/<int:book_id>")
def update_book_route(book_id):
    data = get_json()

    book, error = update_book(book_id, data)

    if error:
        if error in ("book not found", "library not found"):
            return jsonify({"error": error}), HTTP_404_NOT_FOUND
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify(book_to_dict(book)), HTTP_200_OK

@api.patch("/books/<int:book_id>/transfer")
def transfer_book_route(book_id):
    data = get_json()
    new_library_id = data.get("library_id")

    if not new_library_id:
        return jsonify({"error": "library_id is required"}), HTTP_400_BAD_REQUEST

    book, error = transfer_book(book_id, new_library_id)
    if error:
        return jsonify({"error": error}), HTTP_404_NOT_FOUND

    return jsonify(book_to_dict(book)), HTTP_200_OK


@api.delete("/books/<int:book_id>")
def delete_book_route(book_id):
    success, error = delete_book(book_id)

    if error:
        return jsonify({"error": error}), HTTP_404_NOT_FOUND

    return jsonify({"message": "book deleted"}), HTTP_200_OK


@api.get("/books")
def list_books_route():
    filters = {
        "library_id": request.args.get("library_id", type=int),
        "q": request.args.get("q")
    }

    books = list_books(filters)
    return jsonify([book_to_dict(b) for b in books]), HTTP_200_OK


