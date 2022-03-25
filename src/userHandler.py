import uuid
import os
import fileHandler

file = fileHandler.FileHandler("user_data_files", ".txt")


def get_user_and_pass(file_path: str) -> list:
    with open(file_path) as f:
        data = f.readlines(1)[0]
        [user, passwd] = data.split(",")
        return [user, passwd.strip()]


def are_credentials_ok(file_path, user, passwd) -> bool:
    [u, p] = get_user_and_pass(file_path)
    if user == u and passwd == p:
        return True
    else:
        return False


def add_user(user: str, passwd: str) -> bool:
    file_path = file.get_file_path(user)
    if user and passwd:
        if not os.path.exists(file_path):
            fileHandler.write_file(file_path, f"{user},{passwd}\n")
            return True
        else:
            return are_credentials_ok(file_path, user, passwd)
    return False


def get_hash(user: str) -> uuid.UUID:
    user_hash = uuid.uuid4()
    file_path = file.get_file_path(user)
    fileHandler.update_file(file_path, f"{user_hash}\n")
    return user_hash
