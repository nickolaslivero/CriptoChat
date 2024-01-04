import socketio
from encrypt import encrypt_message, decrypt_message, generate_3des_key

from login import login
from chat import choose_chat


sio = socketio.Client()
user = None
current_room = None

@sio.event
def connect():
    print("Conectado ao servidor")

@sio.event
def disconnect():
    print("Desconectado do servidor")

@sio.on("chat_message")
def handle_chat_message(data):
    print(data)

@sio.on("message")
def handle_message(msg):
    # print("Mensagem criptografada:", msg["encrypted_message"])
    decrypted_message = decrypt_message(msg["encrypted_message"], msg["key"])
    print(f"{msg['user']}: ", decrypted_message)

if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    headers = {"Content-Type": "application/json"}
    symmetric_key = generate_3des_key()

    sio.connect(server_url)

    user = login(server_url, headers)

    while True:
        chosen_user_id, chosen_username = choose_chat(server_url, headers, user["user_id"])

        users = [user["username"], chosen_username]
        users.sort()
        current_room = f"{users[0]}-{users[1]}-room"

        sio.emit("join", {"room": current_room, "username": user["username"]})

        while True:
            message = input()
            if message.lower() == "exit":
                break

            encrypted_message = encrypt_message(message, symmetric_key)
            sio.emit("message", {"user_id": user["user_id"], "encrypted_message": encrypted_message, "user": user["username"],
                                "key": symmetric_key, "room": current_room})

        sio.emit("leave", {"room": current_room, "username": user["username"]})

    sio.disconnect()
