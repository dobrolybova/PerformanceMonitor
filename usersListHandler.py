from result import Result


class UsersListHandler:
    def __init__(self):
        self.users = []
        pass

    def check_passwd_and_add(self, user):
        for u in self.users:
            if u.user == user.user and u.passwd != user.passwd:
                return Result.NOK
        return Result.OK

    def add_user(self, user):
        if not self.users:
            self.users.append(user)
            return Result.OK
        return self.check_passwd_and_add(user)
