import socketio
import random
from encrypt import encrypt_message, decrypt_message

from login import login
from chat import start_chat


sio = socketio.Client()
id = random.randint(0, 100)
current_room = None

@sio.event
def connect():
    print("Conectado ao servidor")

@sio.event
def disconnect():
    print("Desconectado do servidor")

@sio.on("message")
def handle_message(msg):
    if msg["id"] != id and msg["room"] == current_room:
        # print("Mensagem criptografada:", msg["encrypted_message"])
        decrypted_message = decrypt_message(msg["encrypted_message"], msg["iv"])
        print(f"{msg['user']}: ", decrypted_message)

if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    headers = {"Content-Type": "application/json"}
    sio.connect(server_url)

    user = login(server_url, headers)
    chosen_user_id, chosen_username = start_chat(server_url, headers, user["user_id"])

    users = [user["username"], chosen_username]
    users.sort()
    current_room = f"{users[0]}-{users[1]}-room"

    while True:
        message = input()
        if message.lower() == "exit":
            break

        encrypted_message, iv = encrypt_message(message)
        sio.emit("message", {"id": id, "encrypted_message": encrypted_message, "user": user["username"],
                             "iv": iv, "room": current_room})

    sio.disconnect()
