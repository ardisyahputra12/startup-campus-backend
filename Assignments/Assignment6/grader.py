from functools import wraps
from uuid import uuid4
import requests

from sqlalchemy import create_engine, text

import traceback


# you can only change this variable
YOUR_IP = "34.87.145.185"


def grader(f: callable):
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


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
class COL:
    PASS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"


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


def assert_include(
    expression, expected, exc_type=AssertionError, hide: bool = False, err_msg=None
):
    try:
        if expected in expression:
            return
        else:
            errs = [err_msg] if err_msg else []
            if hide:
                expected = "<hidden>"
            err = "\n".join([*errs, f"> there is no {expected} in  {expression}"])
            raise exc_type(err)
    except Exception:
        raise


def assert_response(
    method: str,
    endpoint: str,
    json: dict = None,
    exp_json=None,
    exp_code: int = None,
):
    response = method(endpoint, json=json)
    print(response.json())
    assert_eq(response.json(), exp_json)
    assert_eq(response.status_code, exp_code)


def assert_response_include(
    method: str,
    endpoint: str,
    exp_json=None,
    exp_code: int = None,
):
    response = method(endpoint)
    print(response.json())
    assert_include(response.json(), exp_json)
    assert_eq(response.status_code, exp_code)


HOST = f"http://{YOUR_IP}:5000"


def run_query(query, commit: bool = False):
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        "users",
        "password",
        YOUR_IP,
        "5432",
        "library-db",
    )
    engine = create_engine(engine_uri, future=True)
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]


@grader
def test_endpoint():
    title = f"new_title{str(uuid4())}"
    run_query("delete from books", commit=True)
    with safe_init(70):
        pass

    with Scorer(35, "Test endpoint"):
        assert_response(
            requests.post,
            f"{HOST}/book",
            json={"title": title},
            exp_json={"message": f"Book {title} is added"},
            exp_code=201,
        )
        assert_response(
            requests.post,
            f"{HOST}/borrow",
            json={"name": "Jane", "title": title},
            exp_json={"message": f"Book {title} is borrowed by Jane"},
            exp_code=200,
        )
        assert_response_include(
            requests.get,
            f"{HOST}/book",
            exp_json={"borrower": "Jane", "title": title},
            exp_code=200,
        )
        assert_response(
            requests.post,
            f"{HOST}/return",
            json={"name": "Jane", "title": title},
            exp_json={"message": f"Book {title} is returned safely"},
            exp_code=200,
        )

    with Scorer(35, "Test connect db"):
        data = run_query("select * from books")
        print(data)
        assert_eq(data, [{"title": title, "borrower": None}])


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Assignment 6...")
    tests = [test_endpoint]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Assignment 4:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score}"
    )
