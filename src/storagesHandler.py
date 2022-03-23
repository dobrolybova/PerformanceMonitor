from result import Result


class StoragesHandler:
    def __init__(self):
        self.storages = []

    def add(self, storage):
        self.storages.append(storage)

    def post_data(self, received_data):
        try:
            received_hash = received_data['hash']
        except KeyError:
            return Result.NOK
        for storage in self.storages:
            if storage.get_user_hash() == received_hash:
                storage.post(received_data)
                return Result.OK
        return Result.NOK

    def get_data(self, received_data):
        time_range = received_data
        try:
            received_hash = received_data.to_dict().get('hash')
        except KeyError:
            return None
        for storage in self.storages:
            if str(storage.get_user_hash()) == str(received_hash):
                return storage.get(time_range)
        return None
