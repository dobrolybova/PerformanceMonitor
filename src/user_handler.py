import uuid
import os
import file_handler
from typing import Tuple
from logs_handler import get_logger

file = file_handler.FileHandler("user_data_files", ".txt")
logger = get_logger(__name__)


def get_user_and_pass(file_path: str) -> Tuple[str, str]:
    with open(file_path) as f:
        data = f.readline()
        user, passwd = data.split(",")
    return user, passwd.strip()


def are_credentials_ok(file_path: str, user: str, passwd: str) -> bool:
    if not os.path.exists(file_path):
        return False
    u, p = get_user_and_pass(file_path)
    return user == u and passwd == p


def is_user_valid(user: str, passwd: str) -> bool:
    file_path = file.get_file_path(user)
    return are_credentials_ok(file_path, user, passwd)


def add_user(user: str, passwd: str) -> bool:
    logger.info("Add new user")
    file_path = file.get_file_path(user)
    if os.path.exists(file_path):
        return False
    file_handler.write_file(file_path, f"{user},{passwd}\n")
    return True


def get_hash(user: str) -> uuid.UUID:
    user_hash = uuid.uuid4()
    file_path = file.get_file_path(user)
    file_handler.update_file(file_path, f"{user_hash}\n")
    return user_hash
