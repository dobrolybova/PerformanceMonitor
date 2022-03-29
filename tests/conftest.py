import pytest
from main import app


@pytest.fixture()
def srv():
    return app


@pytest.fixture()
def client(srv):
    return app.test_client()
