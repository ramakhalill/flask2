from flask import Blueprint, request, jsonify
from app.controllers.userController import create_user, get_user_book_count, update_user, delete_user
from app.http.httpstatus import HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST

api_users = Blueprint("users", __name__)

def get_json():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}

def user_to_dict(user):
    return {"id": user.id, "name": user.name}

@api_users.post("/users")
def create_user_route():
    data = get_json()
    user, error = create_user(data)
    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST
    return jsonify(user_to_dict(user)), HTTP_201_CREATED

@api_users.patch("/users/<int:user_id>")
def update_user_route(user_id):
    data = get_json()
    user, error = update_user(user_id, data)
    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST
    return jsonify(user_to_dict(user)), HTTP_200_OK

@api_users.delete("/users/<int:user_id>")
def delete_user_route(user_id):
    success, error = delete_user(user_id)
    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST
    return jsonify({"message": "user deleted"}), HTTP_200_OK


@api_users.get("/users/<int:user_id>/books/count")
def user_book_count_route(user_id):
    count, error = get_user_book_count(user_id)
    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST
    return jsonify({"count": count}), HTTP_200_OK


