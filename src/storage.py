import os
import json


storge_data_files = "storge_data_files"
cur_path = os.path.dirname(os.path.abspath(__file__))
storage_path = os.path.join(cur_path, storge_data_files)

os.makedirs(storage_path, exist_ok=True)
file_type = ".csv"


def get_file_path(user_hash: str) -> str:
    return f"{os.path.join(storage_path, user_hash)}{file_type}"


def add_user_storage(user_hash: str) -> None:
    file_path = get_file_path(user_hash)
    with open(file_path, "w"):
        pass


def convert_file_storage_to_list(data: str) -> list:
    res = []
    for token in data.split(";"):
        if token is not '':
            res.append(json.loads(token))
    return res


def is_hash_valid(other: str) -> bool:
    for filename in os.listdir(storage_path):
        if filename == f"{other}{file_type}":
            return True
    return False


def post(data) -> None:
    file_name = data["hash"]
    file_path = get_file_path(file_name)
    with open(file_path, "a") as f:
        f.write(json.dumps(data) + ";")


def get(user_hash: str, time_range) -> list:
    file_path = get_file_path(user_hash)
    with open(file_path) as f:
        data = f.readlines()
    cpu_list = [[i['cpu'], i['time']] for i in convert_file_storage_to_list(data[0])]
    return cpu_list


def post_data(user_hash, data) -> bool:
    if is_hash_valid(user_hash):
        post(data)
        return True
    return False


def get_data(user_hash: str, time_range=None) -> list:
    if is_hash_valid(user_hash):
        return get(user_hash, time_range)
    return []


