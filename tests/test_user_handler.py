import user_handler
from unittest.mock import patch
import uuid
import os
import file_handler


class TestUserHandler:
    @patch.object(uuid, "UUID")
    @patch.object(file_handler, "update_file")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_get_hash(self, mock_file, mock_file_handler, mock_uuid):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_ok.txt")
        mock_uuid.return_value = "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        mock_file_handler.return_value = None
        assert user_handler.get_hash("user") == "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        mock_file_handler.assert_called_once()
        mock_uuid.assert_called_once()

    @patch.object(os.path, "exists")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_add_user_already_exist(self, mock_file, mock_exists):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_ok.txt")
        mock_exists.return_value = True
        assert not user_handler.add_user("user", "passwd")

    @patch.object(file_handler, "write_file")
    @patch.object(os.path, "exists")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_add_user(self, mock_file, mock_exists, mock_write_file):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_ok.txt")
        mock_exists.return_value = False
        mock_write_file.return_value = None
        assert user_handler.add_user("user", "passwd")
        mock_write_file.assert_called_once()

    @patch.object(os.path, "exists")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_is_user_valid_file_not_exist(self, mock_file, mock_exists):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_ok.txt")
        mock_exists.return_value = False
        assert not user_handler.is_user_valid("user", "passwd")

    @patch.object(os.path, "exists")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_is_user_valid_wrong_user_file(self, mock_file, mock_exists):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_nok.txt")
        mock_exists.return_value = True
        try:
            user_handler.is_user_valid("user", "passwd")
            assert False
        except ValueError:
            assert True

    @patch.object(os.path, "exists")
    @patch.object(file_handler.FileHandler, "get_file_path")
    def test_is_user_valid(self, mock_file, mock_exists):
        test_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files_directory")
        mock_file.return_value = os.path.join(test_dir_path, "user_ok.txt")
        mock_exists.return_value = True
        assert user_handler.is_user_valid("user", "passwd")




