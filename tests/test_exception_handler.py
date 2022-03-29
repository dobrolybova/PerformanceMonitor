import exception_handler
from http import HTTPStatus


class TestException:
    def test_auth_error(self):
        err = exception_handler.APIAuthError()
        assert err.code == HTTPStatus.FORBIDDEN
        assert err.description == "Authentication Error"
