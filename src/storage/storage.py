import uuid
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class AbcStorage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_hash(self, user_name: str) -> uuid.UUID:
        pass

    @abstractmethod
    def add_user(self, user_name: str, passwd: str) -> None:
        pass

    @abstractmethod
    def is_user_exist(self, user_name: str) -> bool:
        pass

    @abstractmethod
    def is_user_valid(self, user_name: str, passwd: str) -> bool:
        pass

    @abstractmethod
    def is_hash_valid(self, other: str) -> bool:
        pass

    @abstractmethod
    def get_user_data(self, user_hash: str, time_range=None) -> List[Dict[str, float]]:
        pass

    @abstractmethod
    def store_user_data(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def create_user_session(self, user_hash: str) -> None:
        pass


class Storage:
    def __init__(self, storage: AbcStorage):
        self.storage = storage

    def get_hash(self, user_name: str) -> uuid.UUID:
        return self.storage.get_hash(user_name)

    def add_user(self, user_name: str, passwd: str) -> bool:
        return self.storage.add_user(user_name, passwd)

    def is_user_exist(self, user_name: str) -> bool:
        return self.storage.is_user_exist(user_name)

    def is_user_valid(self, user_name: str, passwd: str) -> bool:
        return self.storage.is_user_valid(user_name, passwd)

    def is_hash_valid(self, other: str) -> bool:
        return self.storage.is_hash_valid(other)

    def get_user_data(self, user_hash: str, time_range=None) -> List[Dict[str, float]]:
        return self.storage.get_user_data(user_hash, time_range)

    def store_user_data(self, data: Dict[str, Any]) -> None:
        return self.storage.store_user_data(data)

    def create_user_session(self, user_hash: str) -> None:
        return self.storage.create_user_session(user_hash)

