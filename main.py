import socketio
import random
import time

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
        print('Mensagem recebida:', msg["message"])

if __name__ == '__main__':
    server_url = 'http://192.168.219.22:5000'
    sio.connect(server_url)

    while True:
        message = input('Digite uma mensagem (ou "exit" para sair): ')
        if message.lower() == 'exit':
            break
        sio.emit('message', {'id': id, 'message': message})

    sio.disconnect()