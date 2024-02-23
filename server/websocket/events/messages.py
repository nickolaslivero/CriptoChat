from app import socketio
from models import Chat

def get_users_in_chat(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()

    if chat:
        users_in_chat = chat.users
        return users_in_chat
    else:
        return []


@socketio.on("message")
def handle_message(data):
    users_in_chat = get_users_in_chat(data["chat_id"])
    for user in users_in_chat:
        socketio.emit("message", data, include_self=False, to=user.username)

@socketio.on("have_received")
def have_received(data):
    socketio.emit("alert_message", data["recipient"], to=data["sender"]["username"])
