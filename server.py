from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# CORS(app)
cors = CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
ws = SocketIO(app)

@ws.on('message')
def handle_message(msg):
    print('Mensagem recebida:', msg)
    ws.emit('message', msg)

if __name__ == '__main__':
    ws.run(app, host="0.0.0.0")
