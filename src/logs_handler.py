from logging import Logger, getLogger, basicConfig
import os


def make_logs_dir(log_dir_name) -> str:
    pid = os.getpid()
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    dir_name = os.path.join(target_path, log_dir_name)
    os.makedirs(dir_name, exist_ok=True)
    return os.path.join(dir_name, str(pid).join([str(pid), ".log"]))


def set_log_level(file_name, log_level) -> None:
    basicConfig(filename=file_name, filemode="w", level=log_level)


def set_imported_modules_log_level(log_level) -> None:
    getLogger('werkzeug').setLevel(log_level)


def get_logger(name: str) -> Logger:
    return getLogger(name)


