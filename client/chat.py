import json
import requests


def choose_chat(server_url, headers, current_user_id):
    response = requests.get(f"{server_url}/user", headers=headers)
    users = json.loads(response.content.decode("utf-8"))

    print("Choose a user to start a chat")

    for user in users:
        if user["user_id"] != current_user_id:
            print(f"{user['user_id']} - {user['username']}")

    chosen_user_ids = input("User ID or IDs (to create a group): ").split(" ")

    return [int(id) for id in chosen_user_ids]
