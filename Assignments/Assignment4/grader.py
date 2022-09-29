"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
import os
import traceback
from functools import wraps
from json import dumps

from sqlalchemy import create_engine, event, text

##############################################################################################
# Helpers
##############################################################################################


def grade(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
        print("-" * 100)
        print(f.__name__)
        print("-" * 100)
        global MAX_SCORE, FINAL_SCORE
        MAX_SCORE, FINAL_SCORE = 0, 0
        try:
            f(*args, **kwargs)
        finally:
            res = FINAL_SCORE, MAX_SCORE
            # reset final score before returning
            FINAL_SCORE = 0
            return res

    return dec


def assert_eq(
    expression, expected, exc_type=AssertionError, hide: bool = False, err_msg=None
):
    try:
        if expression == expected:
            return
        else:
            errs = [err_msg] if err_msg else []
            if hide:
                expected = "<hidden>"
            err = "\n".join(
                [*errs, f"> Expected: {expected}", f"> Yours: {expression}"]
            )
            raise exc_type(err)
    except Exception:
        raise


def assert_f_eq(f, args=None, kwargs=None, exp=None):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    all_args = [dumps(v) for v in args] + [f"{k}={dumps(v)}" for k, v in kwargs.items()]
    err_msg = f'TEST CASE: {f.__name__}({",".join(all_args)})'
    try:
        res = f(*args, **kwargs)
    except Exception as e:
        raise type(e)(err_msg + "\n" + traceback.format_exc())
    return assert_eq(res, expected=exp, err_msg=err_msg)


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
class COL:
    PASS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"


# special exception when something should've been printed, but wasn't
class DisplayError(Exception):
    pass


class Scorer:
    def __enter__(self):
        pass

    def __init__(self, score: int, desc: str):
        self.score = score
        global MAX_SCORE
        MAX_SCORE += score
        print(f"{COL.BOLD}{desc}{COL.ENDC} ({self.score} pts)")

    def __exit__(self, exc_type, exc_value, exc_tb):
        # add maximum score when passing these statements, otherwise 0
        if not exc_type:
            global FINAL_SCORE
            FINAL_SCORE += self.score
            print(COL.PASS, f"\tPASS: {self.score} pts", COL.ENDC)
        else:
            err_lines = [exc_type.__name__, *str(exc_value).split("\n")]
            errs = [
                "\t" + (" " * 4 if index else "") + line
                for index, line in enumerate(err_lines)
            ]
            print("{}{}".format(COL.WARNING, "\n".join(errs)))
            print(f"\t{COL.FAIL}FAIL: 0 pts", COL.ENDC)

        # skip throwing the exception
        return True


class safe_init:
    def __enter__(self):
        pass

    def __init__(self, max_score: int):
        self.max_score = max_score

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(traceback.format_exc())
            global MAX_SCORE
            MAX_SCORE = self.max_score
            return False

        return True


##############################################################################################
# Actual Tests
##############################################################################################


def assert_response(
    c,
    method: str,
    endpoint: str,
    json: dict = None,
    exp_json=None,
    exp_code: int = None,
):
    response = getattr(c, method)(endpoint, json=json)
    assert_eq(response.json, exp_json)
    assert_eq(response.status_code, exp_code)


@grade
def test_p1():
    with safe_init(10):
        from p1 import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    with Scorer(4, "Valid case"):
        assert_response(
            c, "get", "/area?length=10&width=3", exp_json={"area": 30}, exp_code=200
        )
        assert_response(
            c, "get", "/area?length=4&width=4", exp_json={"area": 16}, exp_code=200
        )

    with Scorer(3, "Length < Width"):
        assert_response(
            c,
            "get",
            "/area?length=3&width=10",
            exp_json={"error": "Length should not be shorter than width"},
            exp_code=400,
        )
        assert_response(
            c,
            "get",
            "/area?length=1&width=2",
            exp_json={"error": "Length should not be shorter than width"},
            exp_code=400,
        )

    with Scorer(3, "Non-positive Width/length"):
        assert_response(
            c,
            "get",
            "/area?length=-1&width=5",
            exp_json={"error": "Both length and with must be positive numbers"},
            exp_code=400,
        )
        assert_response(
            c,
            "get",
            "/area?length=8&width=0",
            exp_json={"error": "Both length and with must be positive numbers"},
            exp_code=400,
        )


@grade
def test_p2():
    with safe_init(20):
        from p2 import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    with Scorer(2, "Initial candies"):
        assert_response(
            c, "get", "/candies", exp_json={"message": "I have 0 candies"}, exp_code=200
        )

    with Scorer(2, "Initial chocolates"):
        assert_response(
            c,
            "get",
            "/chocolates",
            exp_json={"message": "I have 0 chocolates"},
            exp_code=200,
        )

    with Scorer(2, "Add candy"):
        assert_response(
            c,
            "post",
            "/gifts",
            json={"candy": 1},
            exp_json={"message": "Gifts are well received!"},
            exp_code=201,
        )

    with Scorer(2, "Add chocolate"):
        assert_response(
            c,
            "post",
            "/gifts",
            json={"chocolate": 1},
            exp_json={"message": "Gifts are well received!"},
            exp_code=201,
        )

    with Scorer(2, "No candy/chocolates are given"):
        assert_response(
            c,
            "post",
            "/gifts",
            json={},
            exp_json={"error": "No gifts for today :("},
            exp_code=400,
        )

    with Scorer(3, "Check candy/chocolate"):
        assert_response(
            c, "get", "/candies", exp_json={"message": "I have 1 candy"}, exp_code=200
        )
        assert_response(
            c,
            "get",
            "/chocolates",
            exp_json={"message": "I have 1 chocolate"},
            exp_code=200,
        )

    with Scorer(3, "Add more candies and chocolates"):
        assert_response(
            c,
            "post",
            "/gifts",
            json={"candy": 2, "chocolate": 3},
            exp_json={"message": "Gifts are well received!"},
            exp_code=201,
        )
        assert_response(
            c,
            "post",
            "/gifts",
            json={"candy": 5},
            exp_json={"message": "Gifts are well received!"},
            exp_code=201,
        )
        assert_response(
            c,
            "post",
            "/gifts",
            json={"chocolate": 2},
            exp_json={"message": "Gifts are well received!"},
            exp_code=201,
        )

    with Scorer(2, "Check final candies"):
        assert_response(
            c, "get", "/candies", exp_json={"message": "I have 8 candies"}, exp_code=200
        )

    with Scorer(2, "Check final chocolates"):
        assert_response(
            c,
            "get",
            "/chocolates",
            exp_json={"message": "I have 6 chocolates"},
            exp_code=200,
        )


@grade
def test_p3():
    # remove DB if already exists
    db_name = "p3.db"
    if os.path.isfile(db_name):
        os.remove(db_name)

    with safe_init(20):
        from p3 import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    with Scorer(2, "First user registration"):
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Adam", "password": "Eve12345"},
            exp_json={"message": "Registration successful"},
            exp_code=201,
        )

    with Scorer(2, "Missing username/password"):
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Adam"},
            exp_json={"error": "Username or password is not given"},
            exp_code=400,
        )
        assert_response(
            c,
            "post",
            "/register",
            json={"password": "Eve12345"},
            exp_json={"error": "Username or password is not given"},
            exp_code=400,
        )

    with Scorer(5, "Fail to re-register with the same user"):
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Adam", "password": "54321evE"},
            exp_json={"error": "This username has been registered"},
            exp_code=409,
        )

    with Scorer(6, "Invalid password"):
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Bruno", "password": "nt_e4sy"},
            exp_json={"error": "Password must contain at least 8 characters"},
            exp_code=400,
        )
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Bruno", "password": ""},
            exp_json={"error": "Password must contain at least 8 characters"},
            exp_code=400,
        )
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Bruno", "password": "not_easy"},
            exp_json={"error": "Password must contain a number"},
            exp_code=400,
        )

    with Scorer(2, "2nd user registration"):
        assert_response(
            c,
            "post",
            "/register",
            json={"username": "Bruno", "password": "n0t_e4sy"},
            exp_json={"message": "Registration successful"},
            exp_code=201,
        )

    with Scorer(4, "Successful login"):
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "Adam", "password": "Eve12345"},
            exp_json={"message": "Login successful"},
            exp_code=200,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "Bruno", "password": "n0t_e4sy"},
            exp_json={"message": "Login successful"},
            exp_code=200,
        )

    with Scorer(2, "Missing username/password"):
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "Adam"},
            exp_json={"error": "Username or password is not given"},
            exp_code=400,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"password": "Eve12345"},
            exp_json={"error": "Username or password is not given"},
            exp_code=400,
        )

    with Scorer(3, "Login with unregistered user"):
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "adam", "password": "54321evE"},
            exp_json={"error": "Username is not registered"},
            exp_code=401,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "bruno", "password": "n0t_e4sy"},
            exp_json={"error": "Username is not registered"},
            exp_code=401,
        )

    with Scorer(4, "Login with a wrong password"):
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "Adam", "password": "54321eve"},
            exp_json={"error": "Wrong password"},
            exp_code=401,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": "Bruno", "password": "n0t_easy"},
            exp_json={"error": "Wrong password"},
            exp_code=401,
        )


@grade
def test_p4():
    import p4


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Assignment 4...")
    tests = [
        test_p1,
        test_p2,
        test_p3,
        # test_p4
    ]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Assignment 4:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
