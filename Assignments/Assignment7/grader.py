"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
import os
import traceback
from functools import wraps
from json import dumps
from typing import List

from sqlalchemy import create_engine, event, text

from dags.creds import destination_creds

import cases


##############################################################################################
# Helpers
##############################################################################################


def grade(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
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


##############################################################################################
# Actual Tests
##############################################################################################
engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    destination_creds["user"],
    destination_creds["pass"],
    "localhost",
    destination_creds["port"],
    destination_creds["db"],
)

engine = create_engine(engine_uri, future=True)


def run_query(query: str, commit=False):
    with engine.connect() as conn:
        if commit:
            try:
                conn.execute(text(query))
                conn.commit()
            except Exception:
                pass
        else:
            return [dict(row) for row in conn.execute(text(query))]


def count_table(table_name: str) -> int:
    return run_query(f"select count(*) from {table_name}")[0]["count"]


@grade
def test_importing_data():
    with Scorer(5, "most_watched_videos"):
        assert_eq(
            run_query("select * from most_watched_videos limit 70"),
            cases.most_watched_videos,
        )
    # with Scorer(5, "most_active_users"):
    #     assert_eq(
    #         run_query("select * from most_active_users limit 70"),
    #         cases.most_active_users,
    #     )
    with Scorer(5, "least_watched_categories"):
        assert_eq(
            run_query("select * from least_watched_categories limit 70"),
            cases.least_watched_categories,
        )


@grade
def test_transforming_data():
    def check_table(name: str):
        run_query(f"SELECT * FROM {name} limit 1")

    def assert_row_count(name: str, expected: str):
        cnt = run_query(f"SELECT COUNT(*) AS c FROM {name}")[0]["c"]
        assert_eq(cnt, expected, err_msg="Number of rows don't match")

    def check_table_content(name: str, nrows: int, columns: List[str]):
        # assert rows
        assert_row_count(name, nrows)

        # assert columns
        first_row = run_query(f"SELECT * FROM {name} limit 1")[0]
        assert_eq(set(first_row.keys()), set(columns), "Different set of columns")

    with Scorer(3, "Check table users"):
        # check existence of table users
        check_table("users")

    with Scorer(5, "Check content table users"):
        check_table_content(
            "users", 1000, ["user_id", "name", "password", "followers", "registered_at"]
        )

    with Scorer(3, "Check table categories"):
        # check existence of table categories
        check_table("categories")

    with Scorer(4, "Check content table categories"):
        check_table_content(
            "categories",
            15,
            ["ID", "Category name"],
        )

    with Scorer(3, "Check table videos"):
        # check existence of table videos
        check_table("videos")

    with Scorer(5, "Check content table videos"):
        check_table_content(
            "videos",
            1000,
            ["video_id", "title", "length (min)", "category_id", "created_at"],
        )

    with Scorer(3, "Check table views"):
        # check existence of table views
        check_table("views")

    with Scorer(5, "Check content table views"):
        check_table_content(
            "views",
            20000,
            ["view_id", "user_id", "video_id", "started_at", "finished_at"],
        )


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Assignment 7...")
    tests = [test_transforming_data, test_importing_data]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Assignment 7:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
