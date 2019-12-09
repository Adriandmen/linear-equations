import string
import random
import datetime
import time

from sympy.parsing.sympy_parser import parse_expr

from flask import Flask, render_template, make_response, request, abort, jsonify
from flask import Response

from lib.config.config import config
from lib.database.db import db, cursor
from lib.equations.Equation import Equation
from lib.equations.LinearEquations import LinearEquations
from lib.equations.LinearUtils import LinearUtils
from lib.models.ProgressModel import ProgressModel
from lib.models.UserModel import UserModel
from lib.rating.Glicko import Glicko
from lib.rating.Result import Result

app = Flask(__name__)


STANDARD_DEVIATION = 50


def get_history(curr_id):
    cursor.execute("""
            SELECT * FROM progress WHERE UserID IN (SELECT ID FROM users WHERE RandomID = '{}') 
            ORDER BY ID DESC 
            LIMIT 10
            OFFSET 1;
        """.format(curr_id))

    results = cursor.fetchall()
    i = 0
    resp = {}
    for x in results:
        resp["history-{}".format(i)] = {}
        resp["history-{}".format(i)]["correct"] = x[3]
        resp["history-{}".format(i)]["gain"] = x[4]
        resp["history-{}".format(i)]["id"] = x[2]
        i += 1

    return resp


def new_equation(user: UserModel):
    eq = LinearEquations.random_equation(user.rating)
    cursor.execute(
        "INSERT INTO equations (LeftEquation, RightEquation, Variable, Rating) VALUES (%s, %s, %s, %s)",
        (str(eq.left), str(eq.right), str(eq.variables[0]), eq.rating))
    db.commit()
    eq.id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO progress (UserID, EquationID, StartDate) VALUES (%s, %s, %s)",
        (user.id, eq.id, time.strftime('%Y-%m-%d %H:%M:%S'))
    )
    db.commit()
    return eq


@app.route("/")
def index():
    user_randomid = None

    if 'curr_id' not in request.cookies:
        user_rating = 1400
        user_kfactor = 350
        user_randomid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

        cursor.execute("INSERT INTO users (Rating, KFactor, RandomID) VALUES ({}, {}, '{}')".format(
            user_rating,
            user_kfactor,
            user_randomid
        ))
        db.commit()

        print(cursor.rowcount, "record inserted.")

    cursor.execute("SELECT * FROM users AS u WHERE u.RandomID = '{}'".format(request.cookies.get('curr_id', default=user_randomid)))
    user = UserModel.from_tuple(cursor.fetchone())

    print("User:", user)

    cursor.execute(
        "SELECT * FROM progress AS p WHERE p.UserID = {} AND p.Correct IS NULL LIMIT 1".format(user.id)
    )

    curr = cursor.fetchall()
    if curr:
        progress = ProgressModel.from_model(curr[0])
        cursor.execute("SELECT * FROM equations AS e WHERE e.ID = {}".format(progress.equation_id))
        equation = cursor.fetchall()
        eq = Equation.from_model(equation[0])

    else:
        eq = new_equation(user)

    resp = make_response(
        render_template("index.html",
                        rating=round(user.rating, 1),
                        problem_rating=eq.rating))  # type: Response

    if user_randomid is not None:
        resp.set_cookie(key="curr_id", value=user_randomid, expires=datetime.datetime(2020, 1, 1))

    return resp


@app.route("/api/check", methods=['POST'])
def check_answer():
    if 'curr_id' not in request.cookies:
        return abort(500)

    data = request.json
    id = request.cookies.get("curr_id")

    cursor.execute("SELECT * FROM users AS u WHERE u.RandomID = '{}' LIMIT 1".format(id))
    user = UserModel.from_tuple(cursor.fetchall()[0])

    cursor.execute("""SELECT * 
                      FROM equations AS e 
                      WHERE e.ID IN (
                          SELECT EquationID 
                          FROM progress AS p 
                          WHERE p.UserID = {} AND p.Correct IS NULL
                      ) LIMIT 1;
                   """.format(user.id))

    curr_eq = cursor.fetchall()

    if not curr_eq:
        return abort(500)

    eq = Equation.from_model(curr_eq[0])

    solution = eq.solution()
    users_attempt = parse_expr(LinearUtils.to_expr(data["value"]), evaluate=True)
    if solution == users_attempt:
        new_rating = Glicko.new_rating(user.rating, user.kfactor, eq.rating, STANDARD_DEVIATION, Result.Win)
        new_kfactor = Glicko.new_deviation(user.rating, user.kfactor, eq.rating, STANDARD_DEVIATION)
        correct = True
    else:
        new_rating = Glicko.new_rating(user.rating, user.kfactor, eq.rating, STANDARD_DEVIATION, Result.Loss)
        new_kfactor = Glicko.new_deviation(user.rating, user.kfactor, eq.rating, STANDARD_DEVIATION)
        correct = False

    cursor.execute("UPDATE progress "
                   "SET Correct = {}, RatingGain = {}, UserAnswer = '{}' "
                   "WHERE UserID = {} AND EquationID = {}".format(
        correct,
        new_rating - user.rating,
        data["value"],
        user.id,
        eq.id
    ))
    db.commit()

    cursor.execute("UPDATE users SET Rating = {}, KFactor = {} WHERE ID = {}".format(
        new_rating,
        new_kfactor,
        user.id
    ))
    db.commit()

    new_eq = new_equation(user)
    resp = get_history(request.cookies.get("curr_id"))

    return jsonify({
        "newRating": new_rating,
        "correct": correct,
        "equation": {
            "latex": new_eq.to_latex(),
            "variable": str(new_eq.variables[0]),
            "rating": new_eq.rating
        },
        "history": resp
    })


@app.route("/api/current", methods=['GET'])
def get_current():
    if "curr_id" not in request.cookies:
        abort(500)

    cursor.execute("""SELECT * 
                      FROM equations AS e 
                      WHERE e.ID IN (
                          SELECT EquationID 
                          FROM progress AS p 
                          WHERE p.Correct IS NULL AND p.UserID IN (
                              SELECT ID
                              FROM users AS u
                              WHERE u.RandomID = '{}'
                          )
                      ) LIMIT 1;
                   """.format(request.cookies.get("curr_id")))

    curr_eq = cursor.fetchall()

    if not curr_eq:
        return abort(500)

    eq = Equation.from_model(curr_eq[0])
    resp = get_history(request.cookies.get("curr_id"))

    return jsonify({
        "latex": eq.to_latex(),
        "variable": str(eq.variables[0]),
        "rating": eq.rating,
        "history": resp
    })


@app.route("/problem/<int:problem_id>")
def retrieve_problem(problem_id: int):
    if "curr_id" not in request.cookies:
        abort(500)

    cursor.execute(
        """
        SELECT * FROM progress AS p WHERE p.EquationID = {} AND p.UserID IN (
            SELECT ID FROM users AS u WHERE u.RandomID = '{}'
        ) LIMIT 1;
        """.format(problem_id, request.cookies.get("curr_id"))
    )
    progress = ProgressModel.from_model(cursor.fetchall()[0])

    print(progress)

    cursor.execute(
        """
        SELECT * FROM equations AS e WHERE e.ID = {} LIMIT 1;
        """.format(problem_id)
    )
    equation = Equation.from_model(cursor.fetchall()[0])

    def latexify(string: str):
        negative = False
        if string.startswith("-"):
            negative = True
            string = string[1:]

        if "/" in string:
            ss = string.split("/")
            return ("-" if negative else "") + " \\frac{" + str(ss[0]) + "}{" + str(ss[1]) + "}"
        else:
            return ("-" if negative else "") + string

    return render_template("problem.html",
                           problem_rating=equation.rating,
                           problem_id=equation.id,
                           problem_latex=equation.to_latex(),
                           variable=equation.get_var(),
                           user_answer=progress.user_answer,
                           solution_latex=latexify(str(equation.solution())))


if __name__ == '__main__':
    app.run(host=config.get_server_host(), debug=config.get_server_debug())
