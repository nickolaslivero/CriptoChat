from flask_socketio import join_room, leave_room, rooms

from app import socketio


@socketio.on("join")
def on_join(data):
    room = data["room"]
    username = data["username"]
    join_room(room)
    socketio.emit("chat_message", f"{username} entrou no chat", to=room)


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    username = data["username"]
    leave_room(room)
    socketio.emit("chat_message", f"{username} saiu do chat", to=room)
