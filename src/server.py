from flask import Flask, request, Response, json
from http import HTTPStatus
import storage
from userHandler import UserHandler
from usersListHandler import UsersListHandler
import dataValidator


server = Flask(__name__)
user_list = UsersListHandler()


def resp(code, data) -> Response:
    return Response(status=code, response=json.dumps(data))


@server.route('/login', methods=['POST'])
def login() -> Response:
    u = UserHandler(request.json['user'], request.json['passwd'])
    user_hash = u.get_hash()
    if not user_hash:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "No user o password, please provide"})
    if not user_list.add_user(u):
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong password"})
    storage.add_user_storage(str(user_hash))
    return resp(HTTPStatus.OK, {"hash": user_hash})


@server.route('/cpu', methods=['POST'])
def post_cpu() -> Response:
    user_hash = dataValidator.get_uuid_if_valid(request.json)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if storage.post_data(str(user_hash), request.json):
        return resp(HTTPStatus.OK, {"put_data": request.json})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})


@server.route('/cpu', methods=['GET'])
def get_cpu() -> Response:
    timerange = None
    user_hash = dataValidator.get_uuid_if_valid(request.args)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    data = storage.get_data(str(user_hash), timerange)
    if not data:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})
    return resp(HTTPStatus.OK, {"get_data": data})


if __name__ == '__main__':
    server.run(debug=True)
