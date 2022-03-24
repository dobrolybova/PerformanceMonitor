class UsersListHandler:
    def __init__(self):
        self.users = []
        pass

    def check_passwd_and_add(self, user) -> bool:
        for u in self.users:
            if u.user == user.user and u.passwd != user.passwd:
                return False
        return True

    def add_user(self, user) -> bool:
        if not self.users:
            self.users.append(user)
            return True
        return self.check_passwd_and_add(user)
