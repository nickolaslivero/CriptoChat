import socketio

sio = socketio.Client()
sio.connect("http://127.0.0.1:5000")

sio.emit("message", data={
    "encrypted_message": "Esta messagem de teste",
    "user": "manu",
    "chat_id": "3"
})

input()