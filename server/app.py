from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from models import db, User
from routers import status, auth, user, chat

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "secret!"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
cors = CORS(app, resources={r"/socket.io/*": {"origins": "*"}})

db.init_app(app)

# Registering routers
app.register_blueprint(status.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)
app.register_blueprint(chat.bp)

socketio = SocketIO(app)
