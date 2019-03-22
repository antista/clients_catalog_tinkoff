import pytest

from server.models import Client, User


def test_client():
    client = Client(id='1', name='name', phone_number='71112223344', email='kek@kek.ru')
    assert client.name == 'name'
    assert client.phone_number == '71112223344'
    assert client.email == 'kek@kek.ru'
    assert client.id == '1'


def test_create_client():
    user = User('login')
    assert not user.phone_numbers
    assert not user.emails
    assert not user.clients
    client = user.create_client('name', '71112223344', 'kek@kek.ru')
    assert client.name == 'name'
    assert client.phone_number == '71112223344'
    assert client.email == 'kek@kek.ru'
    assert client in user.clients.values()
    assert '71112223344' in user.phone_numbers
    assert 'kek@kek.ru' in user.emails


def test_create_exist_client():
    user = User('login')
    user.create_client('name', '71112223344', 'kek@kek.ru')
    user.create_client('name', '78901234567', 'kekek@kek.ru')
    with pytest.raises(FileExistsError):
        user.create_client('some', '74443332211', 'kek@kek.ru')
        user.create_client('another', '71112223344', 'another@kek.ru')


def test_delete_client():
    user = User('login')
    client = user.create_client('name', '71112223344', 'kek@kek.ru')
    assert user.clients
    assert user.phone_numbers
    assert user.emails
    user.delete_client(client.id)
    assert not user.clients
    assert not user.phone_numbers
    assert not user.emails
