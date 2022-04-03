from flask import Flask, request, Response, json, jsonify
from http import HTTPStatus
from typing import Tuple
from storage_handler import add_user_storage, post_data, get_data
from user_handler import get_hash, add_user, is_user_valid
import exception_handler
from data_validator import validate_credentials, get_uuid_if_valid
from logging import INFO, DEBUG, CRITICAL,  WARNING
from logs_handler import make_logs_dir, set_log_level, set_imported_modules_log_level, get_logger

app = Flask(__name__)
logger = get_logger(__name__)


def main():
    file_name = make_logs_dir("logs")
    set_log_level(file_name, INFO)
    set_imported_modules_log_level(CRITICAL)
    app.run()


def resp(code, data) -> Response:
    return Response(status=code, response=json.dumps(data))


def handle_user_hash(user: str) -> Response:
    user_hash = get_hash(user)
    add_user_storage(str(user_hash))
    return resp(HTTPStatus.OK, {"hash": user_hash})


def get_credentials(data: dict) -> Tuple[str, str]:
    if not validate_credentials(data):
        raise exception_handler.APIAuthError()
    return data['user'], data['passwd']


@app.errorhandler(exception_handler.APIError)
def handle_exception(err):
    response = {"error": err.description}
    return jsonify(response), err.code


@app.route('/register', methods=['POST'])
def register() -> Response:
    logger.info("new user registered")
    user, passwd = get_credentials(request.json)
    u = add_user(user, passwd)
    if not u:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "User is already registered"})
    return handle_user_hash(user)


@app.route('/login', methods=['POST'])
def login() -> Response:
    logger.info("new user is logged in")
    user, passwd = get_credentials(request.json)
    u = is_user_valid(user, passwd)
    if not u:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong credentials or user is not registered"})
    return handle_user_hash(user)


@app.route('/cpu', methods=['POST'])
def post_cpu() -> Response:
    logger.info(f"post cpu request {request.json}")
    user_hash = get_uuid_if_valid(request.json)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if post_data(str(user_hash), request.json):
        return resp(HTTPStatus.OK, {"payload": request.json})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})


@app.route('/cpu', methods=['GET'])
def get_cpu() -> Response:
    timerange = None
    logger.info(f"post get request {request.args}")
    user_hash = get_uuid_if_valid(request.args)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    data = get_data(str(user_hash), timerange)
    if not data:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})
    return resp(HTTPStatus.OK, {"payload": data})


if __name__ == '__main__':
    main()
