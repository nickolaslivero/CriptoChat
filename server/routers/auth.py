from flask import Flask, request, jsonify, Blueprint

from models import User
from app import db


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and data["password"] == user.password:
        return jsonify({"message": "Access confirmed"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
