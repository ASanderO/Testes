# test_app.py

import pytest
from src.app import create_user, get_user, update_user, delete_user, load_data

def setup_function(function):
    with open("db/database.json", "w") as file:
        file.write("[]")

def test_create_user():
    create_user({'id': 1, 'name': 'Teste'})
    assert get_user(1)['name'] == 'Teste'

def test_update_user():
    create_user({'id': 1, 'name': 'Teste Inicial'})  # Primeiro, crie o usuário
    update_user(1, {'name': 'Teste Modificado'})  # Depois, atualize-o
    assert get_user(1)['name'] == 'Teste Modificado'  # Por fim, verifique a atualização


def test_delete_user():
    delete_user(1)
    assert get_user(1) is None

def test_create_multiple_users():
    create_user({'id': 1, 'name': 'Teste 1'})
    create_user({'id': 2, 'name': 'Teste 2'})
    data = load_data()
    assert len(data) == 2
    assert get_user(1)['name'] == 'Teste 1'
    assert get_user(2)['name'] == 'Teste 2'

def test_get_nonexistent_user():
    assert get_user(999) is None

def test_update_nonexistent_user():
    result = update_user(999, {'name': 'No User'})
    assert result is None, "Should return None for non-existent user"

def test_delete_nonexistent_user():
    delete_user(999)
    data = load_data()
    assert len(data) == 0

def test_update_user_partial_data():
    create_user({'id': 3, 'name': 'Teste 3', 'email': 'teste3@teste.com'})
    update_user(3, {'email': 'novoemail@teste.com'})
    updated_user = get_user(3)
    assert updated_user['name'] == 'Teste 3'
    assert updated_user['email'] == 'novoemail@teste.com'

def test_delete_user_reduces_count():
    create_user({'id': 4, 'name': 'Teste 4'})
    create_user({'id': 5, 'name': 'Teste 5'})
    delete_user(4)
    data = load_data()
    assert len(data) == 1
    assert get_user(4) is None
    assert get_user(5) is not None
