from flask import Flask, request, jsonify, Blueprint

from models import User
from app import db


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
def fetch_all_users():
    users = User.query.all()
    data = [{"user_id": user.id, "username": user.username} for user in users]
    return jsonify(data)
