import os


def update_file(file_path: str, data: str) -> None:
    with open(file_path, "a") as f:
        f.write(data)


def write_file(file_path: str, data: str) -> None:
    with open(file_path, "w") as f:
        f.write(data)


class FileHandler:
    def __init__(self, storge_directory: str, file_type: str):
        self.file_type = file_type
        target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.storage_path = os.path.join(target_path, storge_directory)
        os.makedirs(self.storage_path, exist_ok=True)

    def get_file_path(self, user_hash: str) -> str:
        return f"{os.path.join(self.storage_path, user_hash)}{self.file_type}"




