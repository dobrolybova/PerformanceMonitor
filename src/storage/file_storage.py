import csv
import os
import uuid
from logging import getLogger
from typing import List, Dict, Any, Tuple, Optional

from .storage import AbcStorage

logger = getLogger(__name__)


class FileStorage(AbcStorage):
    def __init__(self):
        super().__init__()
        self.user = FileHandler("users", ".txt")
        self.data = FileHandler("users_data", ".csv")

    def get_hash(self,  user_name: str) -> uuid.UUID:
        user_hash = uuid.uuid4()
        self.user.update_file(user_name, f"{user_hash}\n")
        return user_hash

    def add_user(self, user_name: str, passwd: str) -> None:
        logger.info(f"Add new user:{user_name}")
        self.user.write_file(user_name, f"{user_name},{passwd}\n")

    def is_user_exist(self, user_name: str) -> bool:
        if os.path.exists(self.user.get_file_path(user_name)):
            return True
        return False

    def _get_user_and_pass(self, user_name: str) -> Tuple[Optional[str], Optional[str]]:
        if not self.is_user_exist(user_name):
            return None, None
        with open(self.user.get_file_path(user_name)) as f:
            data = f.readline()
            user, passwd = data.split(",")
        return user, passwd.strip()

    def is_user_valid(self, user: str, passwd: str) -> bool:
        u, p = self._get_user_and_pass(user)
        return user == u and passwd == p

    def is_hash_valid(self, other: str) -> bool:
        for filename in os.listdir(self.data.storage_path):
            if filename == f"{other}{self.data.file_type}":
                return True
        return False

    @staticmethod
    def _combine_data_to_values_lists(data_list: List[str]) -> List[Dict[str, float]]:
        return [{"timestamp": float(timestamp), "cpu": float(cpu)} for cpu, timestamp in data_list]

    def get_user_data(self, user_hash: str, time_range=None) -> List[Dict[str, float]]:
        with open(self.data.get_file_path(user_hash)) as f:
            data_list = list(csv.reader(f.readlines()))
        return self._combine_data_to_values_lists(data_list[1:])

    def store_user_data(self, data: Dict[str, Any]) -> None:
        file_name = data["hash"]
        self.data.update_file(file_name, str(data["cpu"]) + "," + str(data["time"]) + "\n")

    def create_user_session(self, user_hash: str) -> None:
        logger.info(f"Add new session:{user_hash}")
        self.data.write_file(user_hash, "cpu,time\n")


class FileHandler:
    def __init__(self, storge_directory: str, file_type: str):
        self.file_type = file_type
        target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
        self.storage_path = os.path.join(target_path, storge_directory)
        os.makedirs(self.storage_path, exist_ok=True)

    def get_file_path(self, user: str) -> str:
        return f"{os.path.join(self.storage_path, user)}{self.file_type}"

    def update_file(self, user: str, data: str) -> None:
        with open(self.get_file_path(user), "a") as f:
            f.write(data)

    def write_file(self, user: str, data: str) -> None:
        with open(self.get_file_path(user), "w") as f:
            f.write(data)
