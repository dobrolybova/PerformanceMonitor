from flask import Flask, request, Response, json
from http import HTTPStatus
import storage_handler
import user_handler
import data_validator


server = Flask(__name__)


def resp(code, data) -> Response:
    return Response(status=code, response=json.dumps(data))


@server.route('/login', methods=['POST'])
def login() -> Response:
    user = request.json['user']
    passwd = request.json['passwd']
    u = user_handler.add_user(user, passwd)
    if not u:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Wrong/no user or password, please provide correct"})
    user_hash = user_handler.get_hash(user)
    storage_handler.add_user_storage(str(user_hash))
    return resp(HTTPStatus.OK, {"hash": user_hash})


@server.route('/cpu', methods=['POST'])
def post_cpu() -> Response:
    user_hash = data_validator.get_uuid_if_valid(request.json)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    if storage_handler.post_data(str(user_hash), request.json):
        return resp(HTTPStatus.OK, {"put_data": request.json})
    return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to post data, please login"})


@server.route('/cpu', methods=['GET'])
def get_cpu() -> Response:
    timerange = None
    user_hash = data_validator.get_uuid_if_valid(request.args)
    if not user_hash:
        return resp(HTTPStatus.BAD_REQUEST, {"reason": "Bad arguments"})
    data = storage_handler.get_data(str(user_hash), timerange)
    if not data:
        return resp(HTTPStatus.UNAUTHORIZED, {"reason": "Not authorized user try to get data, please login"})
    return resp(HTTPStatus.OK, {"get_data": data})


if __name__ == '__main__':
    server.run(debug=True)
