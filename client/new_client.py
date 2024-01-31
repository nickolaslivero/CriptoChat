
from encrypt import encrypt_message, decrypt_message, generate_3des_key
from rsa_encrypt import rsa_encrypt, rsa_decrypt, generate_rsa_keys

import streamlit as st
import requests
import socketio
import requests
import json


server_url = "http://127.0.0.1:5000"
headers = {"Content-Type": "application/json"}

sio = socketio.Client()
sio.connect(server_url)

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
def sent_key_to_server(data):
    global symmetric_key
    encrypted_3des_key = rsa_encrypt(symmetric_key, data["public_key"])
    return encrypted_3des_key

@sio.on("message")
def handle_message(data):
    global public_key, private_key

    def set_key(key):
        decrypted_3des_key = rsa_decrypt(key, private_key)
        print(f"{data['user']}: ", decrypt_message(data["encrypted_message"], decrypted_3des_key))

    sio.emit("get_key", {"sid": data["sid"], "public_key": public_key}, callback=set_key)


if "current_chat" not in st.session_state:
    st.session_state["current_chat"] = None

if "chats" not in st.session_state:
    st.session_state["chats"] = {}

if "is_logged" not in st.session_state:
    st.session_state["is_logged"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = None

if "rsa_keys" not in st.session_state:
    private_key, public_key = generate_rsa_keys()
    st.session_state["rsa_keys"] = {
        "private_key": private_key,
        "public_key": public_key
    }

if "3des_key" not in st.session_state:
    symmetric_key = generate_3des_key()
    st.session_state["3des_key"] = symmetric_key


def login(username, password):
    response = requests.post(f"{server_url}/login", json={"username": username, "password": password}, headers=headers)

    if response.status_code == 200:
        user = json.loads(response.content.decode("utf-8"))["user"]
        return True, user
    else:
        return False, None

def fetch_users():
    response = requests.get(f"{server_url}/user", headers=headers)
    users = json.loads(response.content.decode("utf-8"))
    return users

def load_chat():
    chat = st.session_state.current_chat
    st.title("Chat: " + chat)
    for message in st.session_state.chats[chat]["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def choose_chat(username, user_ids):
    st.session_state.current_chat = username
    if username not in st.session_state["chats"]:
        st.session_state.chats[username] = {"messages": []}

    data = requests.post(f"{server_url}/chat/enter_chat", json={"user_ids": user_ids}, headers=headers).content
    chat_id = json.loads(data.decode("utf-8"))["chat_id"]

    if st.session_state.chat_id:
        sio.emit("leave", {"room": st.session_state.chat_id})

    sio.emit("join", {"room": chat_id, "username": user["username"]})
    st.session_state.chat_id = chat_id

    load_chat()

def add_message_to_chat(chat, content):
    current_chat = st.session_state.current_chat
    st.session_state.chats[chat]["messages"].append({"role": "user", "content": content})
    if current_chat == chat:
        load_chat()

def send_message(content):
    current_chat = st.session_state.current_chat
    add_message_to_chat(current_chat, content)

def receive_message(chat, content):
    add_message_to_chat(chat, content)


if not st.session_state.is_logged:
    placeholder = st.empty()

    with placeholder.container():
        username = st.text_input("Username")
        password = st.text_input("Password")
        if st.button("Logar"):
            st.session_state.is_logged, st.session_state.user = login(username, password)

            if st.session_state.is_logged:
                st.session_state.username = username
                placeholder.empty()
            else:
                st.write("Usuário ou senha errados")

if st.session_state.is_logged:
    with st.sidebar:
        users = fetch_users()
        st.title("Chats")
        for user in users:
            if user["username"] != st.session_state.username:
                st.button(user["username"], on_click=lambda u=user["username"], ui=[st.session_state["user"]["user_id"], user["user_id"]]: choose_chat(u, ui))

    if prompt := st.chat_input("What is up?"):
        send_message(prompt)
