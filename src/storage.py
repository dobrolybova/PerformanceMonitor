import os
import json


storge_data_files = "storge_data_files"


def storage(user_hash) -> None:
    if not os.path.exists("./" + storge_data_files):
        os.makedirs("./" + storge_data_files)
    f = open(f"./{storge_data_files}/{user_hash}.txt", "w")
    f.close()


def convert_file_storage_to_list(data_str) -> list:
    res = []
    for token in data_str.split(";"):
        if token is not '':
            token = token.replace("'", '"')
            res.append(json.loads(token))
    return res


def is_hash_valid(other) -> bool:
    for filename in os.listdir("./" + storge_data_files):
        if filename == f"{other}.txt":
            return True
    return False


def post(data) -> list:
    file_name = data["hash"]
    f = open(f"./{storge_data_files}/{file_name}.txt", "a")
    f.write(f"{str(data)};")
    f.close()


def get(user_hash, time_range) -> list:
    with open(f"./{storge_data_files}/{user_hash}.txt") as f:
        data = f.readlines()
    cpu_list = [[i['cpu'], i['time']] for i in convert_file_storage_to_list(data[0])]
    return cpu_list


def post_data(user_hash, data) -> bool:
    if is_hash_valid(user_hash):
        post(data)
        return True
    return False


def get_data(user_hash, time_range=None) -> list:
    if is_hash_valid(user_hash):
        return get(user_hash, time_range)
    return None


