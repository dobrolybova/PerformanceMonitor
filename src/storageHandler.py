import os
import json
import fileHandler


file = fileHandler.FileHandler("storge_data_files", ".csv")


def add_user_storage(user_hash: str) -> None:
    file_path = file.get_file_path(user_hash)
    fileHandler.write_file(file_path, "cpu,time\n")


def combine_data_to_values_lists(data_list: list) -> list:
    j = []
    k = []
    for i in data_list[1:]:
        j.append(float(i[0]))
        k.append(float(i[1].strip()))
    return [j, k]


def is_hash_valid(other: str) -> bool:
    for filename in os.listdir(file.storage_path):
        if filename == f"{other}{file.file_type}":
            return True
    return False


def post(data: json) -> None:
    file_name = data["hash"]
    file_path = file.get_file_path(file_name)
    fileHandler.update_file(file_path, str(data["cpu"]) + "," + str(data["time"]) + "\n")


def get(user_hash: str, time_range) -> list:
    file_path = file.get_file_path(user_hash)
    with open(file_path) as f:
        data = f.readlines()
    data_list = [i.split(",") for i in data]
    return combine_data_to_values_lists(data_list)


def post_data(user_hash: str, data: json) -> bool:
    if is_hash_valid(user_hash):
        post(data)
        return True
    return False


def get_data(user_hash: str, time_range=None) -> list:
    if is_hash_valid(user_hash):
        return get(user_hash, time_range)
    return []


