from app.extensions import db
from app.models import Book, Library
from sqlalchemy import or_


def create_book(data):
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    library_id = data.get("library_id")

    if not title or not author or not library_id:
        return None, "all the fields are required!"

    library = Library.query.get(library_id)
    if not library:
        return None, "library not found"

    book = Book(
        title=title,
        author=author,
        library_id=library_id
    )
    db.session.add(book)
    db.session.commit()

    return book, None


def update_book(book_id, data):
    book = Book.query.get(book_id)
    if not book:
        return None, "book not found"

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return None, "title cannot be empty"
        book.title = title

    if "author" in data:
        author = (data.get("author") or "").strip()
        if not author:
            return None, "author cannot be empty"
        book.author = author

    if "library_id" in data:
        new_library_id = data.get("library_id")
        if not new_library_id:
            return None, "library_id cannot be empty"

        library = Library.query.get(new_library_id)
        if not library:
            return None, "library not found"

        book.library_id = new_library_id

    db.session.commit()
    return book, None




# WHY NOT   Book.query.delete(book_id)   ??






def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return False, "book not found"

    db.session.delete(book)
    db.session.commit()

    return True, None



def list_books(filters):
    query = Book.query

    library_id = filters.get("library_id")
    q = (filters.get("q") or "").strip()

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if q:
        query = query.filter(or_(
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%")
        ))

    books = query.order_by(Book.created_at.desc()).all()
    return books


def transfer_book(book_id, new_library_id):
    book = Book.query.get(book_id)
    if not book:
        return None, "book not found"

    library = Library.query.get(new_library_id)
    if not library:
        return None, "destination library not found"

    book.library_id = new_library_id
    db.session.commit()
    return book, None
