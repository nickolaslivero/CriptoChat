import os

from flask import json, jsonify, Blueprint
from .generate_keys import decrypt_message

bp = Blueprint("keys", __name__)


@bp.route("/public_key", methods=["GET"])
def public_key():
    master_key = os.getenv("MASTER_KEY").encode("utf-8").decode('unicode_escape').encode('latin1')
    current_dir = os.path.dirname(os.path.realpath(__file__))
    keys_file = os.path.join(current_dir, "keys.json")
    with open(keys_file, "r") as file:
        key_data = json.load(file)
        public_key = key_data["public_key"]
    public_key = decrypt_message(public_key, master_key)
    return jsonify({"public_key": public_key})
