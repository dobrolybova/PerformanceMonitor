from flask import Flask, request, Response, json
from http import HTTPStatus
from storage import Storage
from userHandler import UserHandler
from usersListHandler import UsersListHandler
from result import Result
from storagesHandler import StoragesHandler
from uuid import UUID
import dataValidator


server = Flask(__name__)
storages = StoragesHandler()
user_list = UsersListHandler()


def resp(code, data) -> Response:
    return Response(status=code, response=json.dumps(data))


@server.route('/login', methods=['POST'])
def login() -> Response:
    u = UserHandler(request.json['user'], request.json['passwd'])
    user_hash = u.get_hash()
    if user_hash is None:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "No user o password, please provide"})
    storages.add(Storage(user_hash))
    if user_list.add_user(u) == Result.NOK:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong password"})
    return resp(HTTPStatus.OK, {"hash": user_hash})


@server.route('/cpu', methods=['POST'])
def post_cpu() -> Response:
    user_hash = dataValidator.get_uuid_if_valid(request.json)
    if user_hash is None:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if storages.post_data(user_hash, request.json) == Result.OK:
        return resp(HTTPStatus.OK, {"put_data": request.json})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})


@server.route('/cpu', methods=['GET'])
def get_cpu() -> Response:
    timerange = None
    user_hash = dataValidator.get_uuid_if_valid(request.args)
    if user_hash is None:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    data = storages.get_data(user_hash, timerange)
    if data is None:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})
    return resp(HTTPStatus.OK, {"get_data": data})


if __name__ == '__main__':
    server.run(debug=True)
