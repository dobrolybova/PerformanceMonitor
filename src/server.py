from flask import Flask, request, Response, json
from http import HTTPStatus
from storage import Storage
from userHandler import UserHandler
from usersListHandler import UsersListHandler
from result import Result
from storagesHandler import StoragesHandler

server = Flask(__name__)
storages = StoragesHandler()
user_list = UsersListHandler()


def resp(code, data):
    return Response(status=code, response=json.dumps(data))


@server.route('/login', methods=['POST'])
def login():
    u = UserHandler(request.json['user'], request.json['passwd'])
    user_hash = u.get_hash()
    if user_hash is None:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "No user o password, please provide"})
    storages.add(Storage(user_hash))
    if user_list.add_user(u) == Result.NOK:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong password"})
    return resp(HTTPStatus.OK, {"hash": user_hash})


@server.route('/cpu', methods=['POST'])
def post_cpu():
    data = request.json
    if storages.post_data(data) == Result.OK:
        return resp(HTTPStatus.OK, {"put_data": data})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})


@server.route('/cpu', methods=['GET'])
def get_cpu():
    data = storages.get_data(request.args)
    if data is not None:
        return resp(HTTPStatus.OK, {"get_data": data})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})


if __name__ == '__main__':
    server.run(debug=True)
