import random
import re

from sympy import Symbol, Mul
from typing import Union


class LinearUtils:

    @staticmethod
    def random_int(lower_bound: int, upper_bound: int):
        r = random.randint(lower_bound, upper_bound)

        if r == 0:
            return LinearUtils.random_int(lower_bound, upper_bound)

        return r

    @staticmethod
    def random_strict_int(lower_bound: int, upper_bound: int):
        r = random.randint(lower_bound, upper_bound)

        if r == 0 or r == 1 or r == -1:
            return LinearUtils.random_int(lower_bound, upper_bound)

        return r

    @staticmethod
    def add_or_subtract(left: Union[int, Symbol], right: Union[int, Symbol]):
        operator = random.choice(["+", "-"])

        if operator == "+":
            return left + right
        else:
            return left - right

    @staticmethod
    def multiply_parentheses(left: Symbol, right: Symbol):
        return Mul(left, right, evaluate=False)

    @staticmethod
    def to_latex(string: str) -> str:
        string = string.replace("**", "^")
        string = string.replace("*", " ")
        return string

    @staticmethod
    def to_expr(string: str) -> str:
        return re.sub(r"(\d+)\s+(\d+\s*/\s*\d+)", r"(\1 + \2)", string)


if __name__ == '__main__':
    print(LinearUtils.to_expr("1/3"))

