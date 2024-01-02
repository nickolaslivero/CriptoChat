import json
import requests


def login(server_url, headers):    
    logged = False
    while not logged:
        print("-="*30)
        print("Faça login")
        print("-="*30)
        username = input("username: ")
        password = input("password: ")

        response = requests.post(f"{server_url}/login", json={"username": username, "password": password}, headers=headers)

        if (response.status_code == 200):
            logged = True
            user = json.loads(response.content.decode("utf-8"))["user"]
        else:
            print("\nAlgo deu errado tente novamente")
            print(f"[ERROR] {json.loads(response.content.decode('utf-8'))['message']}")
        print()
    return user
