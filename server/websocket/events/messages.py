from app import socketio


@socketio.on("message")
def handle_message(data):
    socketio.emit("message", data, include_self=False, to=data["room"])
