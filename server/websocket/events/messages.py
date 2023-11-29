from app import socketio


@socketio.on("message")
def handle_message(msg):
    print("Mensagem recebida:", msg)
    socketio.emit("message", msg)
