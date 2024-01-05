from flask import Flask, request, jsonify, Blueprint

from models import Chat, User, user_chat_association
from app import db

bp = Blueprint("chat", __name__, url_prefix="/chat")


def get_chat_if_already_exists(users):
    user_ids = [user.id for user in users]

    existing_chats = (
        Chat.query
        .join(user_chat_association)
        .filter(user_chat_association.c.user_id.in_(user_ids))
        .group_by(Chat.id)
        .having(db.func.count(user_chat_association.c.user_id) == len(users))
        .all()
    )

    for chat in existing_chats:
        if set(user_ids) == set([user.id for user in chat.users]):
            return chat

    return None


def get_or_create_new_chat(users):
    chat = get_chat_if_already_exists(users)
    if not chat:
        chat = Chat()
        for user in users:
            chat.users.append(user)
        db.session.add(chat)
        db.session.commit()
    return chat


@bp.route("/enter_chat", methods=["POST"])
def enter_chat():
    data = request.get_json()
    users = [User.query.get(user_id) for user_id in data["user_ids"]]
    chat = get_or_create_new_chat(users)
    
    if chat:
        return jsonify({"chat_id": chat.id}), 200
    else:
        return jsonify({"error": "Failed to create or find chat"}), 500
