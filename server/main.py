from app import app, socketio

from websocket.events.messages import *

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1")
