class UserModel:

    def __init__(self, id: int, rating: int, kfactor: float, random_id: str, username: str = None):
        self.id = id
        self.rating = rating
        self.kfactor = kfactor
        self.random_id = random_id
        self.username = username

    @staticmethod
    def from_tuple(data: tuple):
        return UserModel(data[0], data[2], data[3], data[4], data[1])

    def __repr__(self):
        return "User({}, {}, {}, {}, {})".format(
            self.id,
            self.username,
            self.rating,
            self.kfactor,
            self.random_id
        )
