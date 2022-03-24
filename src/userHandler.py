import uuid


class UserHandler:
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.hash = None

    def get_hash(self) -> uuid.UUID:
        if self.user is not None and self.passwd is not None:
            self.hash = uuid.uuid4()
        return self.hash
