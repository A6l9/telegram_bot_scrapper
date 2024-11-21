class TempStorage:
    def __init__(self, user_id):
        self.user_id = user_id
        self.keyword = 'Не выбрано'
        self.range_subs = 'Не указано'
        self.amount_min = 0
        self.amount_max = 0


class UserManager:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = TempStorage(user_id)
        return self.users[user_id]