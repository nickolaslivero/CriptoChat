import socketio
import random
from encrypt import encrypt_message, decrypt_message

sio = socketio.Client()
id = random.randint(0, 100)

@sio.event
def connect():
    print('Conectado ao servidor')

@sio.event
def disconnect():
    print('Desconectado do servidor')

@sio.on(f'message')
def handle_message(msg):
    if msg["id"] != id:
        print("Mensagem criptografada:", msg["encrypted_message"])
        decrypted_message = decrypt_message(msg["encrypted_message"], msg["iv"])
        print('Mensagem descriptografada:', decrypted_message)

if __name__ == '__main__':
    server_url = 'http://127.0.0.1:5000'
    sio.connect(server_url)

    while True:
        message = input('Digite uma mensagem (ou "exit" para sair): ')
        if message.lower() == 'exit':
            break
        
        encrypted_message, iv = encrypt_message(message)
        sio.emit('message', {'id': id, 'encrypted_message': encrypted_message, 'iv': iv})

    sio.disconnect()
