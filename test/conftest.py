import pytest
from server import wsgi


@pytest.fixture
def app():
    return wsgi.app


@pytest.fixture(scope='module')
def test_client():
    flask_app = wsgi.app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture()
def headers():
    from requests.auth import _basic_auth_str
    return {'Authorization': _basic_auth_str('username', 'password'), }
