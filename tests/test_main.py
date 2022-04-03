from unittest.mock import patch
from http import HTTPStatus
import main
import time


class TestMain:
    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=False)
    def test_register_wrong_credentials(self, mock_validate_credentials, mock_logs_dir, mock_log_level, client):
        response = client.post("/register", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.data == b'{"error":"Authentication Error"}\n'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=True)
    @patch.object(main, "add_user", return_value=False)
    def test_register_user_already_registered(self, mock_validate_credentials_user, mock_add_user, mock_logs_dir, mock_log_level, client):
        response = client.post("/register", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == b'{"reason": "User is already registered"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=True)
    @patch.object(main, "add_user", return_value=True)
    @patch.object(main, "get_hash", return_value='6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa')
    @patch.object(main, "add_user_storage", return_value=None)
    def test_register_ok(self, mock_validate_credentials_user, mock_add_user, mock_get_hash, mock_add_user_storage, mock_logs_dir, mock_log_level, client):
        response = client.post("/register", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.OK
        assert response.data == b'{"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=False)
    def test_login_wrong_credentials(self, mock_validate_credentials, mock_logs_dir, mock_log_level, client):
        response = client.post("/login", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.data == b'{"error":"Authentication Error"}\n'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=True)
    @patch.object(main, "is_user_valid", return_value=False)
    def test_login_not_valid_user(self, mock_validate_credentials_user, mock_is_user_valid, mock_logs_dir, mock_log_level, client):
        response = client.post("/login", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.data == b'{"reason": "Wrong credentials or user is not registered"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "validate_credentials", return_value=True)
    @patch.object(main, "is_user_valid", return_value=True)
    @patch.object(main, "get_hash", return_value='6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa')
    @patch.object(main, "add_user_storage", return_value=None)
    def test_login_ok(self, mock_validate_credentials_user, mock_is_user_valid,  mock_get_hash, mock_add_user_storage, mock_logs_dir, mock_log_level, client):
        response = client.post("/login", json={"user": "user", "passwd": "password"})
        assert response.status_code == HTTPStatus.OK
        assert response.data == b'{"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=False)
    def test_post_cpu_wrong_hash(self, mock_get_uuid_if_valid, mock_logs_dir, mock_log_level, client):
        response = client.post("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20.0, "time": 1648481187.7068})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == b'{"reason": "Bad arguments"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=True)
    @patch.object(main, "post_data", return_value=False)
    def test_post_cpu_unauthorized(self, mock_get_uuid_if_valid, mock_post_data, mock_logs_dir, mock_log_level, client):
        response = client.post("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20.0, "time": 1648481187.7068})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.data == b'{"reason": "Not authorized user try to post data, please login"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=True)
    @patch.object(main, "post_data", return_value=True)
    def test_post_cpu_ok(self, mock_get_uuid_if_valid, mock_post_data, mock_logs_dir, mock_log_level, client):
        response = client.post("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20.0, "time": 1648481187.7068})
        assert response.status_code == HTTPStatus.OK
        assert response.data == (b'{"payload": {"cpu": 20.0, "hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "time": 1648481187.7068}}')

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=False)
    def test_get_cpu_wrong_hash(self, mock_get_uuid_if_valid,mock_logger, mock_log_level, client):
        time_value = time.time()
        response = client.get("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "time": time_value})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == b'{"reason": "Bad arguments"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=True)
    @patch.object(main, "get_data", return_value=False)
    def test_get_cpu_unauthorized(self, mock_get_uuid_if_valid, mock_get_data, mock_logs_dir, mock_log_level, client):
        time_value = time.time()
        response = client.get("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "time": time_value})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.data == b'{"reason": "Not authorized user try to get data, please login"}'

    @patch.object(main, "set_log_level")
    @patch.object(main, "make_logs_dir")
    @patch.object(main, "get_uuid_if_valid", return_value=True)
    @patch.object(main, "get_data", return_value=[{'cpu': 8.1, 'timestamp': 1648304309.405101}, {'cpu': 5.4, 'timestamp': 1648304310.4123461}])
    def test_get_cpu_ok(self, mock_get_uuid_if_valid, mock_post_data, mock_logger, mock_log_level, client):
        response = client.get("/cpu", json={"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20.0, "time": 1648481187.7068})
        assert response.status_code == HTTPStatus.OK
        assert response.data == (b'{"payload": [{"cpu": 8.1, "timestamp": 1648304309.405101}, {"cpu": 5.4, "timestamp": 1648304310.4123461}]}')
