class User:
    """
    Класс хранения временных данных введенных пользователем
    """
    all_users = dict()
    towns_dict = dict()

    def __init__(self, user_id: int):
        self.city = None
        self.city_gaiaId = None
        self.city_id = None
        self.hotels_amount = None
        self.user_command = None
        self.check_in = []
        self.check_out = []
        self.flag_check_in = False
        self.flag_last_day_month = False
        self.flag_last_month = False
        self.sort_type = None
        self.hotels_list = []
        self.need_to_get_photo = None
        self.price_range = None
        self.distance_range = None
        User.add_user(user_id, self)

    @staticmethod
    def get_user(user_id):
        if not User.all_users.get(user_id):
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @staticmethod
    def del_user(user_id):
        if User.all_users.get(user_id):
            del User.all_users.get[user_id]
