from http import HTTPStatus
from flask import url_for

from server import views
from server.models import User


def test_index(mocker, app, test_client, headers):
    mocker.patch('server.views.get_login', return_value='login')
    mocker.patch('server.views.requires_basic_auth')
    mocker.patch('server.views.authenticate')
    mocker.patch('server.views.check_auth', return_value=True)
    with app.test_request_context():
        response = test_client.get("/", headers=headers)
        assert response.status_code == 302
        assert 'You should be redirected automatically to target URL:' \
               ' <a href="/login">/login</a>.  If not click the link.' \
               in response.data.decode()


def test_authed_index(mocker, app, test_client, headers):
    mocker.patch('server.views.get_login', return_value='login')
    mocker.patch('server.views.requires_basic_auth')
    mocker.patch('server.views.authenticate')
    mocker.patch('server.views.check_auth', return_value=True)
    with app.test_request_context():
        views.sessions['login'] = User('login')
        response = test_client.get("/login", headers=headers)
        assert response.status_code == 200
        assert '<h1>Clients</h1>' in response.data.decode()


def test_check_auth():
    assert views.check_auth('login', 'password')
    assert not views.check_auth('login', 'smth')
    assert views.check_auth('login', 'password')


def test_authentificate_responce():
    responce = views.authenticate()
    assert responce.status_code == 401
    assert 'You have to login' in responce.data.decode()


def test_require_auth(app, mocker):
    mocker.patch('server.views.check_auth', return_value=False)

    @views.requires_basic_auth
    def foo():
        pass

    with app.test_request_context():
        responce = foo()
        assert responce.status_code == 401


def test_get_login(app):
    with app.test_request_context():
        assert views.get_login() is None


def test_authed_index_throw_404(mocker, app, test_client, headers):
    mocker.patch('server.views.get_login', return_value='some_login')
    mocker.patch('server.views.requires_basic_auth')
    mocker.patch('server.views.authenticate')
    mocker.patch('server.views.check_auth', return_value=True)
    with app.test_request_context():
        views.sessions['login'] = User('login')
        response = test_client.get("/login", headers=headers)
        assert response.status_code == 404


def test_index_with_clients(mocker, app, test_client, headers):
    mocker.patch('server.views.get_login', return_value='login')
    mocker.patch('server.views.requires_basic_auth')
    mocker.patch('server.views.authenticate')
    mocker.patch('server.views.check_auth', return_value=True)
    with app.test_request_context():
        user = User('login')
        views.sessions['login'] = user
        response = test_client.get("/login", headers=headers)
        assert response.status_code == 200
        assert '<h1>Clients</h1>' in response.data.decode()
        users_client = user.create_client('client', '71112223344', 'email@io.com')
        response = test_client.get(url_for('authed_index', login='login'), headers=headers)
        assert response.status_code == HTTPStatus.OK
        assert users_client.id[:5] in response.data.decode()


def test_create(mocker, app, test_client, headers):
    mocker.patch('flask.redirect')
    with app.test_request_context():
        test_client.get(url_for('create', login='login'), headers=headers)
        assert views.sessions['login'].clients
        assert '71112223344' in views.sessions['login'].phone_numbers
        assert views.sessions['login'].emails


def test_delete_client(mocker, app, test_client, headers):
    mocker.patch('flask.redirect')
    with app.test_request_context():
        user = User('login')
        views.sessions['login'] = user
        user.create_client('client', '71112223345', 'email@i.com')
        test_client.get(url_for('delete', login='login', client_id=list(user.clients.keys())[0]))
        assert not user.clients
        assert not user.phone_numbers
        assert not user.emails
