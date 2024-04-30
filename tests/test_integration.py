import pytest
from pytest_mock import mocker
from src.app import create_user, get_user, update_user, authenticated_get_user
from src.authentication import authenticate

def test_integration(mocker):
    mocker.patch('src.authentication.authenticate', return_value=True)
    assert authenticate("admin", "secret") is True
    create_user({'id': 2, 'name': 'Integrado'})
    assert get_user(2)['name'] == 'Integrado'

def test_failed_authentication(mocker):
    mocker.patch('src.authentication.authenticate', return_value=False)
    assert authenticate("user", "wrongpassword") is False

def test_create_user_with_authentication(mocker):
    mocker.patch('src.authentication.authenticate', return_value=True)
    if authenticate("admin", "secret"):
        create_user({'id': 6, 'name': 'Admin User'})
        assert get_user(6)['name'] == 'Admin User'
    else:
        assert False, "Authentication Failed, User not created"

def test_access_data_without_authentication(mocker):
    mocker.patch('src.authentication.authenticate', return_value=False)
    with pytest.raises(PermissionError):
        authenticated_get_user(6)  # Deve lançar PermissionError quando a autenticação falhar


def test_update_nonexistent_user():
    result = update_user(999, {'name': 'No User'})
    assert result is None, "Should return None for non-existent user"


def test_update_user_partial_data():
    create_user({'id': 3, 'name': 'Teste 3', 'email': 'teste3@teste.com'})
    update_user(3, {'email': 'novoemail@teste.com'})
    updated_user = get_user(3)
    assert updated_user['name'] == 'Teste 3'
    assert updated_user['email'] == 'novoemail@teste.com'

