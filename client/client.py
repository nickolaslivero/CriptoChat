import socketio
import requests
import json

from encrypt import encrypt_message, decrypt_message, generate_3des_key

from login import login
from chat import choose_chat


sio = socketio.Client()

@sio.event
def connect():
    print("Conectado ao servidor")

@sio.event
def disconnect():
    print("Desconectado do servidor")

@sio.on("chat_message")
def handle_chat_message(data):
    print(data)

@sio.on("send_key_to_server")
def sent_key_to_server():
    global symmetric_key
    return symmetric_key

@sio.on("message")
def handle_message(data):
    def set_key(key):
        print(f"{data['user']}: ", decrypt_message(data["encrypted_message"], key))

    sio.emit("get_key", {"sid": data["sid"]}, callback=set_key)


if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    headers = {"Content-Type": "application/json"}
    symmetric_key = generate_3des_key()

    sio.connect(server_url)

    user = login(server_url, headers)

    while True:
        user_ids = choose_chat(server_url, headers, user["user_id"])
        user_ids.append(int(user["user_id"]))

        data = requests.post(f"{server_url}/chat/enter_chat", json={"user_ids": user_ids}, headers=headers).content

        chat_id = json.loads(data.decode("utf-8"))["chat_id"]

        sio.emit("join", {"room": chat_id, "username": user["username"]})

        while True:
            message = input()
            if message.lower() == "exit":
                break

            encrypted_message = encrypt_message(message, symmetric_key)
            sio.emit("message", {"encrypted_message": encrypted_message, "user": user["username"], "room": chat_id, "sid": sio.sid })

        sio.emit("leave", {"room": chat_id, "username": user["username"]})

    sio.disconnect()
