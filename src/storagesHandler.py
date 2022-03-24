from result import Result


class StoragesHandler:
    def __init__(self):
        self.storages = []

    def add(self, storage) -> list:
        self.storages.append(storage)

    def post_data(self, user_hash, data) -> Result:
        for storage in self.storages:
            if storage.is_hash_valid(user_hash):
                storage.post(data)
                return Result.OK
        return Result.NOK

    def get_data(self, user_hash, time_range=None) -> list:
        for storage in self.storages:
            if storage.is_hash_valid(user_hash):
                return storage.get(time_range)
        return None
