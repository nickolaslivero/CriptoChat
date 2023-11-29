from flask import Blueprint

bp = Blueprint("status", __name__)

@bp.route("/", methods=["GET"])
def is_online():
    return "[Server] Server is running..."
