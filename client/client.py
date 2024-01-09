import socketio
import requests
import json

from encrypt import encrypt_message, decrypt_message, generate_3des_key
from rsa_encrypt import rsa_encrypt, rsa_decrypt, generate_rsa_keys

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
def sent_key_to_server(data):
    global symmetric_key
    print("[INFO] Chave pública recebida: ", data["public_key"])
    print("[INFO] Criptografando chave 3des com a chave pública")
    encrypted_3des_key = rsa_encrypt(symmetric_key, data["public_key"])
    print("[INFO] Enviando chave 3des criptografada: ", encrypted_3des_key)
    return encrypted_3des_key

@sio.on("message")
def handle_message(data):
    global public_key, private_key

    def set_key(key):
        print("[INFO] Chave 3des criptografada recebida: ", key)
        decrypted_3des_key = rsa_decrypt(key, private_key)
        print("[INFO] Descriptografando chave 3des: ", decrypted_3des_key)
        print(f"{data['user']}: ", decrypt_message(data["encrypted_message"], decrypted_3des_key))

    print("[INFO] Mensagem criptografa recebida: ", data["encrypted_message"])
    print("[INFO] Solicitando chave 3des e enviando a chave pública")
    sio.emit("get_key", {"sid": data["sid"], "public_key": public_key}, callback=set_key)


if __name__ == "__main__":
    server_url = "http://127.0.0.1:5000"
    # server_url = "http://149.100.154.93:5000"
    headers = {"Content-Type": "application/json"}
    symmetric_key = generate_3des_key()
    private_key, public_key = generate_rsa_keys()

    print("[INFO] Chave 3des: ", symmetric_key)
    print("[INFO] Chave RSA privada: ", private_key)
    print("[INFO] Chave RSA pública: ", public_key)

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
            print("[INFO] Enviando mesangem criptografada: ", encrypted_message)
            sio.emit("message", {"encrypted_message": encrypted_message, "user": user["username"], "room": chat_id, "sid": sio.sid })

        sio.emit("leave", {"room": chat_id, "username": user["username"]})

    sio.disconnect()
