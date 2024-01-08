from app import socketio

import time


@socketio.on("get_key")
def get_key(data):
    timeout = 10
    key = None

    def set_key(value):
        nonlocal key
        key = value
        print("Set_key: ", key)

    socketio.emit("send_key_to_server", include_self=False, callback=set_key)

    timeout = time.time() + timeout
    while not key and time.time() <= timeout:
        time.sleep(0.1)

    return key
