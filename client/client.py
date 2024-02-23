import socketio
import requests
import json
import os

from encrypt import generate_3des_key, encrypt_message, decrypt_message
from rsa_encrypt import generate_rsa_keys, rsa_encrypt, rsa_decrypt


server_url = "http://127.0.0.1:5000"
headers = {"Content-Type": "application/json"}
sio = socketio.Client()

class SessionState:
    def __init__(self):
        self.user = {}
        self.is_logged = False
        self.current_chat = None
        self.chats = {}

session_state = SessionState()

def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')

def login(username, password):
    response = requests.post(f"{server_url}/login", json={"username": username, "password": password}, headers=headers)

    if response.status_code == 200:
        user = json.loads(response.content.decode("utf-8"))["user"]
        return user
    else:
        return None

def fetch_users():
    response = requests.get(f"{server_url}/user", headers=headers)
    users = json.loads(response.content.decode("utf-8"))
    return users

def show_users(users):
    print("-="*15)
    print("Users in Criptochat")
    for user in users:
        if user["user_id"] != session_state.user["user_id"]:
            print(f"\t{user['user_id']} {user['username']}")
    print("-="*15)

def select_users():
    users = input("Users ids: ")
    users = users.split(" ")
    users.append(session_state.user["user_id"])
    return users

def get_chat_id(users_id):
    data = requests.post(f"{server_url}/chat/enter_chat", json={"user_ids": users_id}, headers=headers).content
    chat_id = json.loads(data.decode("utf-8"))["chat_id"]
    return chat_id

def start_chat(chat_id):
    clear()

    print("[INFO] Chave 3des: ", session_state.chats[chat_id]["symmetric_key"])
    print("[INFO] Chave RSA Privada: ", session_state.chats[chat_id]["rsa_keys"][0])
    print("[INFO] Chave RSA Publica: ", session_state.chats[chat_id]["rsa_keys"][1])

    print(f"Entrou no chat {chat_id}")

    load_chat(chat_id)

    while True:
        message = input()

        if message == "exit":
            session_state.current_chat = None
            break

        send_message(chat_id, message)

    clear()

def load_chat(chat_id):
    for message in session_state.chats[chat_id]["messages"]:
        if message["user"]["user_id"] != session_state.user["user_id"]:
            print(f"{message['user']['username']}: {message['message']}")
        else:
            print(message['message'])

def init_chat_data(chat_id):
    symmetric_key = generate_3des_key()
    rsa_private_key, rsa_public_key = generate_rsa_keys()
    session_state.chats[chat_id] = {
        "messages": [],
        "symmetric_key": symmetric_key,
        "rsa_keys": (rsa_private_key, rsa_public_key),
        "users_keys": {}
    }

def add_message_to_chat(chat_id, message, user):
    if chat_id not in session_state.chats:
        init_chat_data(chat_id)
    session_state.chats[chat_id]["messages"].append({"message": message, "user": user})

def send_message(chat_id, message):
    add_message_to_chat(chat_id, message, session_state.user)

    encrypted_message = encrypt_message(message, session_state.chats[chat_id]["symmetric_key"])

    print("[INFO] 1. Enviando mensagem criptografada: ", encrypted_message)

    sio.emit("message", data={"message": encrypted_message, "user": session_state.user, "chat_id": chat_id})

def receive_message(chat_id, message, user):
    if chat_id == session_state.current_chat:
        print(f"{user['username']}: {message}")
    sio.emit("have_received", data={"sender": user, "recipient": session_state.user})
    add_message_to_chat(chat_id, message, user)

sio.connect(server_url)

@sio.on("send_key_to_server")
def sent_key_to_server(data):
    if data["chat_id"] not in session_state.chats:
        init_chat_data(data["chat_id"])

    symmetric_key = session_state.chats[data["chat_id"]]["symmetric_key"]
    encrypted_key = rsa_encrypt(symmetric_key, data["public_key"])

    print("[INFO] 4. Chave RSA publica recebida: ", data["public_key"])
    print("[INFO] 5. Chave criptografa: ", encrypted_key)

    return {"key": encrypted_key, "from": session_state.user}

@sio.on("alert_message")
def alert_message(data):
    print(f"[SERVER] {data['username']} recebeu a mensagem!")

@sio.on("message")
def handle_message(data):

    if data["chat_id"] not in session_state.chats:
        init_chat_data(data["chat_id"])

    def set_key(key):
        if key["from"]["username"] == data["user"]["username"]:
            print("[INFO] 6. Chave criptofrada recebida: ", key["key"])
            encrypted_key = key["key"]
            symmetric_key = rsa_decrypt(encrypted_key, session_state.chats[data["chat_id"]]["rsa_keys"][0])
            print("[INFO] 7. Descriptografando chave 3des com chave RSA privada: ", symmetric_key)
            session_state.chats[data["chat_id"]]["users_keys"][data["user"]["username"]] = symmetric_key
            message = decrypt_message(data["message"], symmetric_key)
            receive_message(chat_id=data["chat_id"], message=message, user=data["user"])

    print(f"[INFO] 2. Mensagem criptografada recebida de {data['user']['username']}: ", data["message"])

    if not session_state.chats[data["chat_id"]]["users_keys"].get(data["user"]["username"], ""):
        print("[INFO] 3. Solicitando chave 3des enviando a chave RSA publica")

        sio.emit("get_key", {
                "public_key": session_state.chats[data["chat_id"]]["rsa_keys"][1],
                "chat_id": data["chat_id"],
                "user": data["user"],
            },
            callback=set_key,
        )
    else:
        try:
            message = decrypt_message(data["message"], session_state.chats[data["chat_id"]]["users_keys"][data["user"]["username"]])
            receive_message(chat_id=data["chat_id"], message=message, user=data["user"])
        except:
            print("[INFO] 2. Mensagem criptografa recebida: ", data["message"])
            print("[INFO] 3. Solicitando chave 3des enviando a chave RSA publica")

            sio.emit("get_key", {
                    "public_key": session_state.chats[data["chat_id"]]["rsa_keys"][1],
                    "chat_id": data["chat_id"],
                    "user": data["user"],
                },
                callback=set_key,
            )

while True:

    while not session_state.is_logged:
        username = input("Username: ")
        password = input("Password: ")

        user = login(username, password)

        if user:
            session_state.user = user
            session_state.is_logged = True
            break

        print("Wrong username or password")

    sio.emit("join", {"room": session_state.user["username"], "username": session_state.user["username"]})

    show_users(fetch_users())

    while True:
        try:
            users_id = select_users()
            chat_id = get_chat_id(users_id)
            break
        except:
            print("digite um valor válido")
            continue

    if chat_id not in session_state.chats:
        init_chat_data(chat_id)

    session_state.current_chat = chat_id

    start_chat(chat_id)
