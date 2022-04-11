from http import HTTPStatus
from logging import INFO, CRITICAL, getLogger
from typing import Tuple

from flask import Flask, request, Response, json, jsonify

import exception_handler
from data_validator import validate_credentials, get_uuid_if_valid
from logs_handler import make_logs_dir, set_log_level, set_imported_modules_log_level
from storage.file_storage import FileStorage
from storage.db_storage import DbStorage
from storage.storage import Storage

app = Flask(__name__)
logger = getLogger(__name__)
storage = Storage(FileStorage())


def main():
    file_name = make_logs_dir("logs")
    set_log_level(file_name, INFO)
    set_imported_modules_log_level(CRITICAL)
    app.run()


def resp(code, data) -> Response:
    return Response(status=code, response=json.dumps(data))


def create_user_session(user: str) -> Response:
    user_hash = storage.get_hash(user)
    storage.create_user_session(str(user_hash))
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
    if storage.is_user_exist(user):
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "User is already registered"})
    storage.add_user(user, passwd)
    return create_user_session(user)


@app.route('/login', methods=['POST'])
def login() -> Response:
    logger.info("new user is logged in")
    user, passwd = get_credentials(request.json)
    u = storage.is_user_valid(user, passwd)
    if not u:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong credentials or user is not registered"})
    return create_user_session(user)


@app.route('/cpu', methods=['POST'])
def post_cpu() -> Response:
    logger.info(f"post cpu request {request.json}")
    user_hash = get_uuid_if_valid(request.json)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if not storage.is_hash_valid(str(user_hash)):
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})
    storage.store_user_data(request.json)
    return resp(HTTPStatus.OK, {"payload": request.json})


@app.route('/cpu', methods=['GET'])
def get_cpu() -> Response:
    timerange = None
    logger.info(f"post get request {request.args}")
    user_hash = get_uuid_if_valid(request.args)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if not storage.is_hash_valid(str(user_hash)):
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})
    data = storage.get_user_data(str(user_hash), timerange)
    return resp(HTTPStatus.OK, {"payload": data})


if __name__ == '__main__':
    main()
