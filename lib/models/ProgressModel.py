from datetime import date


class ProgressModel:

    def __init__(self, id: int, user_id: int, equation_id: int, start_date: date,
                 solved: bool = None, rating_gain: int = None, user_answer: str = None):
        self.id = id
        self.user_id = user_id
        self.equation_id = equation_id
        self.start_date = start_date
        self.solved = solved
        self.rating_gain = rating_gain
        self.user_answer = user_answer

    @staticmethod
    def from_model(data: tuple):
        return ProgressModel(data[0], data[1], data[2], data[6], data[3], data[4], data[5])

    def __repr__(self):
        return "Progress({}, {}, {}, {}, {}, {}, {})".format(
            self.id,
            self.user_id,
            self.equation_id,
            self.start_date,
            self.solved,
            self.rating_gain,
            self.user_answer
        )
