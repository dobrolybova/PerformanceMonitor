import random


class UserHandler:
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.hash = None

    def get_hash(self):
        if self.user is not None and self.passwd is not None:
            self.hash = random.getrandbits(128)
        return self.hash
