import os
import uuid
from unittest.mock import patch

from storage.file_storage import FileStorage, FileHandler


class TestUserHandler:
    @patch.object(uuid, "UUID")
    @patch.object(FileHandler, "update_file", return_value=None)
    def test_get_hash(self, mock_update_file, mock_uuid):
        mock_uuid.return_value = "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        f_s = FileStorage()
        assert f_s.get_hash("user") == "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        mock_update_file.assert_called_once()
        mock_uuid.assert_called_once()

    @patch.object(FileHandler, "write_file", return_value=None)
    def test_add_user(self, mock_write_file):
        f_s = FileStorage()
        f_s.add_user("user", "passwd")
        mock_write_file.assert_called_once()

    @patch.object(os.path, "exists", return_value=False)
    def test_user_not_exist(self, mock_exists):
        f_s = FileStorage()
        assert not f_s.is_user_exist("user")

    @patch.object(os.path, "exists", return_value=True)
    def test_user_exist(self, mock_exists):
        f_s = FileStorage()
        assert f_s.is_user_exist("user")

    @patch.object(FileStorage, "_get_user_and_pass", return_value=[None, None])
    def test_user_not_valid(self, mock_get_user_and_pass):
        f_s = FileStorage()
        assert not f_s.is_user_valid("user", "passwd")
        mock_get_user_and_pass.assert_called_once()

    @patch.object(FileStorage, "_get_user_and_pass", return_value=["user", "passwd"])
    def test_user_valid(self, mock_get_user_and_pass):
        f_s = FileStorage()
        assert f_s.is_user_valid("user", "passwd")
        mock_get_user_and_pass.assert_called_once()

    @patch.object(os, "listdir", return_value=[])
    def test_hash_not_valid(self, mock_listdir):
        f_s = FileStorage()
        assert not f_s.is_hash_valid("10bba744-04df-48a2-aff7-9d3e68992ce0")

    @patch.object(os, "listdir", return_value=["10bba744-04df-48a2-aff7-9d3e68992ce0.csv"])
    def test_hash_valid(self, mock_listdir):
        f_s = FileStorage()
        assert f_s.is_hash_valid("10bba744-04df-48a2-aff7-9d3e68992ce0")

    @patch.object(FileHandler, "write_file", return_value=None)
    def test_create_user_session(self, mock_write_file):
        f_s = FileStorage()
        f_s.create_user_session("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa")
        mock_write_file.assert_called_once()

    @patch.object(FileHandler, "update_file", return_value=None)
    def test_store_user_data_no_time(self, mock_update_file):
        f_s = FileStorage()
        try:
            f_s.store_user_data({"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20})
        except KeyError:
            assert True
        else:
            assert False

    @patch.object(FileHandler, "update_file", return_value=None)
    def test_store_user_data_no_cpu(self, mock_update_file):
        f_s = FileStorage()
        try:
            f_s.store_user_data({"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "time": 100})
        except KeyError:
            assert True
        else:
            assert False

    @patch.object(FileHandler, "update_file", return_value=None)
    def test_store_user_data_no_hash(self, mock_update_file):
        f_s = FileStorage()
        try:
            f_s.store_user_data({"cpu": 20, "time": 100})
        except KeyError:
            assert True
        else:
            assert False

    @patch.object(FileHandler, "update_file", return_value=None)
    def test_store_user_data_no_hash(self, mock_update_file):
        f_s = FileStorage()
        try:
            f_s.store_user_data({"cpu": 20, "time": 100, "hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"})
        except KeyError:
            assert False
        else:
            assert True
            mock_update_file.assert_called_once()

    @patch.object(FileHandler, "get_file_path")
    def test_get_user_data_wrong_data(self, mock_get_file_path):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_get_file_path.return_value = os.path.join(test_dir_path, "data_nok.csv")
        f_s = FileStorage()
        assert f_s.get_user_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa") == []

    @patch.object(FileHandler, "get_file_path")
    def test_get_user_data(self, mock_get_file_path):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_get_file_path.return_value = os.path.join(test_dir_path, "data_ok.csv")
        f_s = FileStorage()
        assert f_s.get_user_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa") == [{'cpu': 20.0, 'timestamp': 1649596019.895147},{'cpu': 10.0, 'timestamp': 1649596019.895147}]







