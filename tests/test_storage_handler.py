import storage_handler
import file_handler
import os
import csv
from unittest.mock import patch


class TestStorageHandler:
    @patch.object(file_handler, "write_file")
    @patch.object(storage_handler, "file")
    def test_add_user_storage(self, mock_file, mock_write_file):
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_write_file.return_value = None
        storage_handler.add_user_storage("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa")
        assert mock_write_file.call_count == 1

    @patch.object(os, "listdir")
    @patch.object(storage_handler, "file")
    def test_get_data_empty_hash_dir(self, mock_file,  mock_listdir):
        mock_listdir.return_value = []
        data = storage_handler.get_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", time_range=None)
        assert data == []

    @patch.object(os, "listdir")
    @patch.object(storage_handler, "file")
    def test_get_data_wrong_hash_file(self, mock_file, mock_listdir):
        mock_listdir.return_value = "test_directory"
        data = storage_handler.get_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", time_range=None)
        assert data == []

    @patch.object(csv, "reader")
    @patch.object(storage_handler, "file")
    @patch.object(os, "listdir")
    def test_get_data(self, mock_listdir, mock_file, mock_reader):
        mock_listdir.return_value = ["6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa.txt"]
        mock_file.file_type = ".txt"
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_reader.return_value = [{"cpu", "timestamp"}, {20.0, 1648481187.7068}]
        data = storage_handler.get_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", time_range=None)
        assert data == [{'cpu': 1648481187.7068, 'timestamp': 20.0}]
        assert mock_reader.call_count == 1

    @patch.object(file_handler, "update_file")
    @patch.object(os, "listdir")
    @patch.object(storage_handler, "file")
    def test_post_data_empty_hash_dir(self, mock_file,  mock_listdir, mock_update_file):
        mock_listdir.return_value = []
        assert not storage_handler.post_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", {"cpu": 20.0, "time": 1648481187.7068})
        mock_update_file.assert_not_called()

    @patch.object(file_handler, "update_file")
    @patch.object(os, "listdir")
    @patch.object(storage_handler, "file")
    def test_post_data_wrong_hash_file(self, mock_file, mock_listdir, mock_update_file):
        mock_listdir.return_value = "test_directory"
        assert not storage_handler.post_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", {"cpu": 20.0, "time": 1648481187.7068})
        mock_update_file.assert_not_called()

    @patch.object(file_handler, "update_file")
    @patch.object(storage_handler, "file")
    @patch.object(os, "listdir")
    def test_post_data(self, mock_listdir, mock_file, mock_update_file):
        mock_listdir.return_value = ["6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa.txt"]
        mock_file.file_type = ".txt"
        mock_file.get_file_path.return_value = os.path.abspath(__file__)
        mock_update_file.return_value = None
        storage_handler.post_data("6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", {"hash": "6a8d8ae8-5fc1-4df0-93db-1ecb7a9af0aa", "cpu": 20.0, "time": 1648481187.7068})
        mock_update_file.assert_called_once()


