import os, json, base64

from flask import Flask, request, jsonify, Blueprint

from models import User
from app import db
from .generate_keys import rsa_decrypt


bp = Blueprint("auth", __name__)


def decrypt_form_data(encrypted_username, encrypted_password):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    keys_file = os.path.join(current_dir, "keys.json")
    with open(keys_file, "r") as file:
        key_data = json.load(file)
        private_key = key_data["private_key"]
    username = rsa_decrypt(encrypted_username, private_key)
    password = rsa_decrypt(encrypted_password, private_key)
    return username.decode("utf-8"), password.decode("utf-8")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    encrypted_username = base64.b64decode(data["username"])
    encrypted_password = base64.b64decode(data["password"])

    username, password = decrypt_form_data(encrypted_username, encrypted_password)

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!", "user": {"user_id": new_user.id, "username": new_user.username}})


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    encrypted_username = base64.b64decode(data["username"])
    encrypted_password = base64.b64decode(data["password"])

    username, password = decrypt_form_data(encrypted_username, encrypted_password)

    user = User.query.filter_by(username=username).first()

    if user and password == user.password:
        return jsonify({"message": "Access confirmed", "user": {"user_id": user.id, "username": user.username}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
