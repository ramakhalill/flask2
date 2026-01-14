from app.extensions import db
from app.models import User, Library
from app.models import Book


def create_user(data):
    name = (data.get("name") or "").strip()
    if not name:
        return None, "name is required"

    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return user, None


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None, "user not found"

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return None, "name cannot be empty"
        user.name = name

    db.session.commit()
    return user, None


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, "user not found"

    db.session.delete(user)
    db.session.commit()
    return True, None



def get_user_book_count(user_id):
    user = User.query.get(user_id)
    if not user or not user.library:
        return None, "user or library not found"

    count = Book.query.filter_by(library_id=user.library.id).count()
    return count, None
