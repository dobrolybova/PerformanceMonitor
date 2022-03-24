class Storage:
    def __init__(self, user_hash):
        self.user_hash = user_hash
        self.data = []

    def post(self, data) -> list:
        self.data.append(data)

    def get(self, time_range) -> list:
        cpu_list = [[i['cpu'], i['time']] for i in self.data]
        return cpu_list

    def is_hash_valid(self, other) -> bool:
        return self.user_hash == other

