from app.extensions import db
from app.models import Library

def create_library(data):
    name = (data.get("name") or "").strip()

    if not name:
        return None, "name is required"

    lib = Library(name=name)
    db.session.add(lib)
    db.session.commit()

    return lib, None

def update_library(library_id, data):
    lib = Library.query.get(library_id)
    if not lib:
        return None, "library not found"

    name = data.get("name")
    if name is not None:
        name = name.strip()
        if not name:
            return None, "name cannot be empty"
        lib.name = name

    db.session.commit()
    return lib, None




def delete_library(library_id):
    lib = Library.query.get(library_id)
    if not lib:
        return False, "library not found"

    db.session.delete(lib)
    db.session.commit()
    return True, None

