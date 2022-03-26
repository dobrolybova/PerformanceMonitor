import os
import file_handler
from typing import List, Dict, Any
import csv

file = file_handler.FileHandler("storge_data_files", ".csv")


def add_user_storage(user_hash: str) -> None:
    file_path = file.get_file_path(user_hash)
    file_handler.write_file(file_path, "cpu,time\n")


def combine_data_to_values_lists(data_list: List[str]) -> List[Dict[str, float]]:
    return [{"timestamp": float(timestamp), "cpu": float(cpu)} for cpu, timestamp in data_list]


def is_hash_valid(other: str) -> bool:
    for filename in os.listdir(file.storage_path):
        if filename == f"{other}{file.file_type}":
            return True
    return False


def post(data: Dict[str, Any]) -> None:
    file_name = data["hash"]
    file_path = file.get_file_path(file_name)
    file_handler.update_file(file_path, str(data["cpu"]) + "," + str(data["time"]) + "\n")


def get(user_hash: str, time_range) -> List[Dict]:
    file_path = file.get_file_path(user_hash)
    with open(file_path) as f:
        data_list = list(csv.reader(f.readlines()))
    return combine_data_to_values_lists(data_list[1:])


def post_data(user_hash: str, data: Dict[str, Any]) -> bool:
    if is_hash_valid(user_hash):
        post(data)
        return True
    return False


def get_data(user_hash: str, time_range=None) -> List[Dict[str, float]]:
    if is_hash_valid(user_hash):
        return get(user_hash, time_range)
    return []
