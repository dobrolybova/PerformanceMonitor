import os
from unittest.mock import patch

from storage.file_storage import FileHandler


class TestFileHandler:
    @patch.object(os.path, "join")
    def test_file_handler(self, mock_join):
        test_dir = "test_dir"
        test_file_type = ".txt"
        mock_join.return_value = test_dir
        fh = FileHandler(test_dir, test_file_type)
        assert fh.file_type == test_file_type
        assert fh.storage_path == test_dir
        assert fh.get_file_path('10bba744-04df-48a2-aff7-9d3e68992ce0') == test_dir + test_file_type
