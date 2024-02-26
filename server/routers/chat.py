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


def get_or_create_new_chat(users, chat_name):
    chat = get_chat_if_already_exists(users)
    if not chat:
        chat = Chat()
        chat.name = chat_name
        for user in users:
            chat.users.append(user)
        db.session.add(chat)
        db.session.commit()
    return chat


def get_user_chats(user_id):
    user = User.query.get(user_id)
    if user:
        return user.chats
    else:
        return None


@bp.route("/enter_chat", methods=["POST"])
def enter_chat():
    data = request.get_json()
    users = [User.query.get(user_id) for user_id in data["user_ids"]]
    chat = get_or_create_new_chat(users, data.get("name", None))
    
    if chat:
        return jsonify({"chat_id": chat.id}), 200
    else:
        return jsonify({"error": "Failed to create or find chat"}), 500


@bp.route("/chats", methods=["POST"])
def chats():
    data = request.get_json()
    user_id = data["user"]["user_id"]
    chats = get_user_chats(user_id)
    data = {
        "chats": []
    }
    for chat in chats:
        if chat.name != None:
            data["chats"].append({
                "id": chat.id,
                "name": chat.name
            })
    return jsonify(data)
