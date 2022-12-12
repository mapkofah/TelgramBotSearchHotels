class User:
    """
    Класс хранения временных данных введенных пользователем
    """
    all_users = dict()
    towns_dict = dict()

    def __init__(self, user_id: int):
        self.amount_photo = None
        self.city = None
        self.city_id = None
        self.data_id = 1
        self.date_message = None
        self.day_in = None
        self.day_out = None
        self.distance_range = None
        self.flag_distance = False
        self.flag_last_day_month = False
        self.flag_last_month = False
        self.hotels_dict = {}
        self.hotels_names = []
        self.month_in = None
        self.month_out = None
        self.need_to_get_photo = False
        self.page_num = 0
        self.list_page_nums = []
        self.price_range = None
        self.page_size = None
        self.user_command = None
        self.year_in = None
        self.year_out = None
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
            User.all_users.pop(user_id)

