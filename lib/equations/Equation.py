from typing import List
from sympy import Symbol, linsolve, symbols, solve

from lib.equations.LinearUtils import LinearUtils


class Equation:

    def __init__(self, left, right, variables: List[Symbol], rating: int, id: int = None):
        self.id = id
        self.left = left
        self.right = right
        self.variables = variables
        self.rating = rating

    def to_latex(self):
        return "{} = {}".format(LinearUtils.to_latex(str(self.left)), LinearUtils.to_latex(str(self.right)))

    def get_left(self):
        if type(self.left) is str:
            exec("{0} = symbols('{0}')".format(self.variables[0]))
            left = eval(self.left)
        else:
            left = self.left
        return left

    def get_right(self):
        if type(self.right) is str:
            exec("{0} = symbols('{0}')".format(self.variables[0]))
            right = eval(self.right)
        else:
            right = self.right
        return right

    def solvable(self) -> bool:
        solutions = list(linsolve([self.get_left() - self.get_right()], self.variables))

        if not solutions:
            return False

        if type(solutions[0][0]) is Symbol:
            return False

        return True

    def get_var(self):
        return str(self.variables[0])

    def solution(self):
        return list(linsolve([self.get_left() - self.get_right()], self.variables))[0][0]

    @staticmethod
    def from_model(data: tuple):
        exec("{0} = symbols('{0}')".format(data[3]))
        left = eval(data[1])
        right = eval(data[2])
        rating = data[4]

        return Equation(left, right, [eval(data[3])], rating, id=data[0])

    def __repr__(self):
        return "Equation({}, {}, {}, {})".format(self.left, self.right, self.variables, self.rating)
