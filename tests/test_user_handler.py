import user_handler
from unittest.mock import patch
import uuid
import os
import storage_handler
import file_handler


class TestUserHandler:
    @patch.object(uuid, "UUID")
    @patch.object(file_handler, "update_file")
    @patch.object(storage_handler, "file")
    def test_get_hash(self, mock_file, mock_file_handler, mock_uuid):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_uuid.return_value = "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        mock_file_handler.return_value = None
        assert user_handler.get_hash("user") == "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa"
        mock_file_handler.assert_called_once()
        mock_uuid.assert_called_once()

    @patch.object(os.path, "exists")
    @patch.object(storage_handler, "file")
    def test_add_user_already_exist(self, mock_file, mock_exists):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_exists.return_value = True
        assert not user_handler.add_user("user", "passwd")

    @patch.object(file_handler, "write_file")
    @patch.object(os.path, "exists")
    @patch.object(storage_handler, "file")
    def test_add_user(self, mock_file, mock_exists, mock_write_file):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_exists.return_value = False
        mock_write_file.return_value = None
        assert user_handler.add_user("user", "passwd")
        mock_write_file.assert_called_once()

    @patch.object(os.path, "exists")
    @patch.object(storage_handler, "file")
    def test_is_user_valid_file_not_exist(self, mock_file, mock_exists):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_exists.return_value = False
        assert not user_handler.is_user_valid("user", "passwd")

    @patch.object(os.path, "exists")
    @patch.object(storage_handler, "file")
    def test_is_user_valid(self, mock_file, mock_exists):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_exists.return_value = True
        assert user_handler.is_user_valid("user", "passwd")




