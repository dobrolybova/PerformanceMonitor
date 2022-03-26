from http import HTTPStatus


class APIError(Exception):
    pass


class APIAuthError(APIError):
    code = HTTPStatus.FORBIDDEN
    description = "Authentication Error"
