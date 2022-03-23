class Storage:
    def __init__(self, user_hash):
        self.user_hash = user_hash
        self.data = []

    def post(self, data):
        self.data.append(data)

    def get(self, time_range):
        cpu_list = [[i['cpu'], i['time']] for i in self.data]
        return cpu_list

    def get_user_hash(self):
        return self.user_hash


