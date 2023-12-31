from app import app, socketio, db

from websocket.events.messages import *
from websocket.events.room import *
from websocket.events.key import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True, host="127.0.0.1")
