from flask import Flask, request, jsonify, Blueprint

from models import Chat
from app import db


bp = Blueprint("chat", __name__, url_prefix="/chat")


@bp.route("/", methods=["GET"])
def fetch_all_chats():
    chats = Chat.query.all()
    data = [{"id": chat.id, "user_1_id": chat.user_1_id, "user_2_id": chat.user_2_id} for chat in chats]
    return jsonify(data)

@bp.route("/", methods=["POST"])
def create_chat():
    data = request.get_json()
    new_chat = Chat(user_1_id=data["user_1_id"], user_2_id=data["user_2_id"])
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"message": "Chat created successfully!"})
