from flask import Blueprint, request, jsonify
from database.services.user_service import create_user, get_users, get_user

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.post("/")
def add_user():
    user = create_user(request.json)
    return jsonify(user), 201


@bp.get("/")
def list_users():
    limit = request.args.get("limit", type=int)
    return jsonify(get_users(limit))


@bp.get("/<identifier>")
def get_single_user(identifier):
    try:
        identifier = int(identifier)
    except ValueError:
        pass

    user = get_user(identifier)
    if not user:
        return {"error": "User not found"}, 404

    return jsonify(user)