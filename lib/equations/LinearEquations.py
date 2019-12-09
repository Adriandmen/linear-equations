import random
from sympy import symbols
from lib.equations.Equation import Equation
from lib.equations.LinearUtils import LinearUtils


def random_noise(range: int) -> int:
    return random.randint(-range, range)


def pm() -> str:
    return random.choice(["+", "-"])


class LinearEquations:

    LETTERS = ["a", "b", "c", "d", "e", "g", "h", "j", "k", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

    @staticmethod
    def random_equation(rating: int):
        rating = rating + random.randint(-45, 45)

        if rating < 1300:
            return LinearEquations.level_1()
        elif rating < 1400:
            return LinearEquations.level_2()
        elif rating < 1500:
            return LinearEquations.level_3()
        elif rating < 1600:
            return LinearEquations.level_4()
        elif rating < 1700:
            return LinearEquations.level_5()
        elif rating < 1800:
            return LinearEquations.level_6()
        elif rating < 1900:
            return LinearEquations.level_7()
        elif rating < 2000:
            return LinearEquations.level_8()
        elif rating < 2100:
            return LinearEquations.level_9()
        elif rating < 2200:
            return LinearEquations.level_10()

        return LinearEquations.level_10()

    @staticmethod
    def level_1() -> Equation:
        v = symbols(random.choice(LinearEquations.LETTERS))
        n1 = LinearUtils.random_int(-3, 4)
        n2 = LinearUtils.random_int(-10, 10)

        left = LinearUtils.add_or_subtract(v * n1, n2)
        right = 0
        curr_equation = Equation(left, right, [v], 1300 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 3:
            return LinearEquations.level_1()

        return curr_equation

    @staticmethod
    def level_2() -> Equation:
        v = symbols(random.choice(LinearEquations.LETTERS))
        n1 = LinearUtils.random_int(-3, 4)
        n2 = LinearUtils.random_int(-10, 10)
        n3 = LinearUtils.random_int(-20, 20)

        left = LinearUtils.add_or_subtract(v * n1, n2)
        right = n3
        curr_equation = Equation(left, right, [v], 1400 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 3:
            return LinearEquations.level_2()

        return curr_equation

    @staticmethod
    def level_3() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v1 = symbols(random_letter)
        n1 = LinearUtils.random_int(-10, 10)
        n2 = LinearUtils.random_int(-3, 4)
        n3 = LinearUtils.random_int(-10, 10)

        left = LinearUtils.add_or_subtract(v1, n1)
        right = LinearUtils.add_or_subtract(n2 * v1, n3)
        curr_equation = Equation(left, right, [v1], 1500 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 3:
            return LinearEquations.level_3()

        return curr_equation

    @staticmethod
    def level_4() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v1 = symbols(random_letter)
        n1 = LinearUtils.random_int(-10, 10)
        n2 = LinearUtils.random_int(-5, 5)
        n3 = LinearUtils.random_int(-10, 10)
        n4 = LinearUtils.random_int(-5, 5)

        left = LinearUtils.add_or_subtract(n2 * v1, n1)
        right = LinearUtils.add_or_subtract(n4 * v1, n3)
        curr_equation = Equation(left, right, [v1], 1600 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 3:
            return LinearEquations.level_4()

        return curr_equation

    @staticmethod
    def level_5() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v1 = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-6, 6)
        n2 = LinearUtils.random_int(-10, 10)
        n3 = LinearUtils.random_int(-5, 5)
        n4 = LinearUtils.random_int(-4, 4)

        left = f"{n1}*({LinearUtils.add_or_subtract(v1, n2)})"
        right = LinearUtils.add_or_subtract(n3 * v1, n4)

        curr_equation = Equation(left, right, [v1], 1700 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_5()

        return curr_equation

    @staticmethod
    def level_6() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-6, -2)
        n2 = LinearUtils.random_int(-10, -1)
        n3 = LinearUtils.random_int(2, 10)
        n4 = LinearUtils.random_int(-4, 4)

        left = f"{n1} * ({v - n2})"
        right = f"{n3} * ({LinearUtils.add_or_subtract(n4, v)})"

        curr_equation = Equation(left, right, [v], 1800 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_6()

        return curr_equation

    @staticmethod
    def level_7() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-6, 6)
        n2 = LinearUtils.random_int(-4, 4)
        n3 = LinearUtils.random_int(-10, 10)
        n4 = LinearUtils.random_int(2, 4)
        n5 = LinearUtils.random_int(-10, 10)
        n6 = LinearUtils.random_int(-4, 4)
        n7 = LinearUtils.random_int(-10, 10)

        left = f"{ n1 } * ({ LinearUtils.add_or_subtract(n2 * v, n3) }) { pm() } { n4 } * ({ LinearUtils.add_or_subtract(v, n5) })"
        right = LinearUtils.add_or_subtract(n6 * v, n7)

        curr_equation = Equation(left, right, [v], 1900 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_7()

        return curr_equation

    @staticmethod
    def level_8() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_int(-4, 4)
        n2 = LinearUtils.random_int(1, 10)
        n3 = LinearUtils.random_int(-4, 4)

        left = f"({ LinearUtils.add_or_subtract(v, n1) }) ** 2 - { n2 * v }"
        right = f"{ v } * ( {n3} + {v} )"

        curr_equation = Equation(left, right, [v], 2000 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_8()

        return curr_equation

    @staticmethod
    def level_9() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-5, 5)
        n2 = LinearUtils.random_strict_int(-5, 5)
        n3 = LinearUtils.random_int(1, 10)
        n4 = LinearUtils.random_int(-10, 10)
        n5 = LinearUtils.random_int(-5, 5)

        left = f"({ LinearUtils.add_or_subtract(v, n1) }) * ({ LinearUtils.add_or_subtract(v, n2) }) { pm() } {n3}"
        right = f"{ n4 } - { v } * ( {n5} - {v} )"

        curr_equation = Equation(left, right, [v], 2100 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_9()

        return curr_equation

    @staticmethod
    def level_10() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-5, 5)
        n2 = LinearUtils.random_int(1, 10)
        n3 = LinearUtils.random_int(-10, 10)
        n4 = LinearUtils.random_int(2, 4)
        n5 = LinearUtils.random_int(-5, 5)
        n6 = LinearUtils.random_int(1, 10)

        left = f"{n1} * {v} - ({v} {pm()} {n2}) * ({n3} - {n4 ** 2 * v})"
        right = f"{n5} + ({n4} * {v} {pm()} {n6}) ** 2"

        curr_equation = Equation(left, right, [v], 2230 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_10()

        return curr_equation

    @staticmethod
    def level_11() -> Equation:
        random_letter = random.choice(LinearEquations.LETTERS)
        v = symbols(random_letter)
        n1 = LinearUtils.random_strict_int(-10, 10)
        n2 = LinearUtils.random_int(1, 10)
        n3 = LinearUtils.random_int(-10, 10)
        n4 = LinearUtils.random_int(4, 9)
        n5 = LinearUtils.random_int(-15, 15)
        n6 = LinearUtils.random_int(10, 20)

        left = f"{n1} * {v} - ({v} {pm()} {n2}) * ({n3} - {n4 ** 2 * v})"
        right = f"{n5} + ({n4} * {v} {pm()} {n6}) ** 2"

        curr_equation = Equation(left, right, [v], 2300 + random_noise(30))

        if not curr_equation.solvable() or len(str(abs(curr_equation.solution()))) > 4:
            return LinearEquations.level_11()

        return curr_equation


if __name__ == '__main__':
    eq = LinearEquations.level_11()
    print(eq.left)
    print(eq.right)
    print(eq.solution())
