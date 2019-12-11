from models import Users


class UserService:  # TODO: create a way to hash passwords
    def __init__(self):
        self.users = Users()

    def create(self, username, password, api_number):
        self.users.add_user(username, password, api_number)
        return "okay"

    def correct_user(self, username):
        if self.users.user_exists(username):
            return True
        else:
            return False

    def correct_log_in(self, username, password):
        return self.users.login(username, password)


