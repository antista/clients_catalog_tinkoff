import pytest
from server import wsgi


@pytest.fixture
def app():
    return wsgi.app
