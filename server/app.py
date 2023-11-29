from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from routers import status

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "secret!"
cors = CORS(app, resources={r"/socket.io/*": {"origins": "*"}})

# Registering routers
app.register_blueprint(status.bp)

socketio = SocketIO(app)
