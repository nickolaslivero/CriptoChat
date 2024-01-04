import json
import requests

def choose_chat(server_url, headers, current_user_id):
    response = requests.get(f"{server_url}/user", headers=headers)
    users = json.loads(response.content.decode("utf-8"))

    print("Choose a user to start a chat")

    for user in users:
        if user["user_id"] != current_user_id:
            print(f"{user['user_id']} - {user['username']}")
    
    chosen_user_id = input("User ID: ")
    chosen_username = None
    for user in users:
        if user["user_id"] == int(chosen_user_id):
            chosen_username = user["username"]

    print(f"Iniciando chat com {chosen_username}")

    return chosen_user_id, chosen_username
