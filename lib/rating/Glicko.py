import math

from lib.rating.Result import Result

q = math.log(10) / 400


def g(deviation_opponent: float) -> float:
    return 1 / (math.sqrt(1 + (3 / math.pow(math.pi, 2)) * (q ** 2) * (deviation_opponent ** 2)))


def E(curr_rating: float, rating_opponent: float, deviation_opponent: float) -> float:
    return 1 / (1 + math.pow(10, (g(deviation_opponent) * (curr_rating - rating_opponent)) / -400))


def inverse_d(deviation_opponent: float, curr_rating: float, rating_opponent: float) -> float:
    E_i = E(curr_rating, rating_opponent, deviation_opponent)
    return (q ** 2) * (g(deviation_opponent) ** 2) * E_i * (1 - E_i)


class Glicko:

    @staticmethod
    def new_rating(rating: float, rd: float, r_opponent: float, rd_opponent: float, result: Result) -> float:
        expected = g(rd_opponent) * (result - E(rating, r_opponent, rd_opponent))
        return rating + (q / ((1 / (rd ** 2)) + inverse_d(rd_opponent, rating, r_opponent))) * expected

    @staticmethod
    def new_deviation(rating: float, rd: float, r_opponent: float, rd_opponent):
        return max(math.sqrt(1 / ((1 / (rd ** 2)) + inverse_d(rd_opponent, rating, r_opponent))), 75)


if __name__ == '__main__':
    r = 1500
    rd = 350
    for _ in range(0, 5):
        r = Glicko.new_rating(r, rd, 1400, 50, Result.Draw)
        rd = Glicko.new_deviation(r, rd, 1400, 50)
        print("New rating is {}".format(r))
        print("New deviation is {}".format(rd))
        print()
