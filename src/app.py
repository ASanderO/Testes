import json
from .authentication import authenticate

def load_data():
    with open("db/database.json", "r") as file:
        return json.load(file)

def save_data(data):
    with open("db/database.json", "w") as file:
        json.dump(data, file, indent=4)

def create_user(user_data):
    data = load_data()
    data.append(user_data)
    save_data(data)

def get_user(user_id):
    data = load_data()
    return next((user for user in data if user['id'] == user_id), None)

def update_user(user_id, new_data):
    data = load_data()
    user = next((user for user in data if user['id'] == user_id), None)
    if not user:
        return None  # Usuário não encontrado, retorna None

    # Atualiza os dados do usuário encontrado
    user.update(new_data)
    save_data(data)
    return user  # Retorna o usuário atualizado

def delete_user(user_id):
    data = load_data()
    data = [user for user in data if user['id'] != user_id]
    save_data(data)


def authenticated_get_user(user_id):
    if not authenticate("username", "password"):
        raise PermissionError("Authentication failed")
    return get_user(user_id)
