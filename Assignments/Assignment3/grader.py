"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
import os
import traceback
from functools import wraps
from json import dumps
from typing import List

from sqlalchemy import create_engine, event, text

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


@grade
def test_explore():
    import explore

    with Scorer(3, "count_users"):
        assert_eq(explore.count_users(), 1000, hide=True)

    with Scorer(5, "count_videos"):
        for case in cases.count_videos:
            assert_f_eq(explore.count_videos, [case[0]], exp=case[-1])

    with Scorer(5, "oldest_videos"):
        for case in cases.oldest_videos:
            assert_f_eq(explore.oldest_videos, [case[0]], exp=case[-1])

    with Scorer(7, "most_watched_videos"):
        for case in cases.most_watched_videos:
            assert_f_eq(explore.most_watched_videos, [case[0]], exp=case[-1])

    with Scorer(12, "most_active_users"):
        for case in cases.most_active_users:
            assert_f_eq(explore.most_active_users, [case[0]], exp=case[-1])

    with Scorer(10, "most_watched_categories"):
        for case in cases.least_watched_categories:
            assert_f_eq(explore.least_watched_categories, [case[0]], exp=case[-1])


@grade
def test_migrate():
    import migrate

    db_name = "assignment3.db"

    with Scorer(3, "Create SQLite DB"):
        migrate.create_sqlite_db()
        if not os.path.isfile(db_name):
            raise FileNotFoundError(f"{db_name} not found")

    engine = create_engine(f"sqlite:///{db_name}", future=True)
    event.listen(engine, "connect", lambda c, _: c.execute("pragma foreign_keys=on"))

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

    run_query("DROP TABLE IF EXISTS views", commit=True)
    run_query("DROP TABLE IF EXISTS videos", commit=True)
    run_query("DROP TABLE IF EXISTS users", commit=True)
    run_query("DROP TABLE IF EXISTS categories", commit=True)

    with Scorer(3, "Create table users"):
        migrate.create_table_users()
        # check existence of table users
        check_table("users")

    with Scorer(5, "Copy users from PostgreSQL to SQLite"):
        migrate.copy_users()
        check_table_content(
            "users", 1000, ["user_id", "name", "password", "followers", "registered_at"]
        )

    with Scorer(7, "Check constraint on users"):
        insert_stmt = (
            "INSERT INTO users(user_id, name, password, followers, registered_at)"
        )
        # null values
        run_query(
            f"{insert_stmt} VALUES(NULL, 'abc', 'abc', 123, '2020-10-01')", commit=True
        )
        run_query(
            f"{insert_stmt} VALUES('xyz', NULL, 'abc', 123, '2020-10-01')", commit=True
        )
        run_query(
            f"{insert_stmt} VALUES('xyz', 'abc', NULL, 123, '2020-10-01')", commit=True
        )
        run_query(
            f"{insert_stmt} VALUES('xyz', 'abc', 'abc', 123, NULL)",
            commit=True,
        )

        # unique
        run_query(
            f"{insert_stmt} VALUES('a4ca07d3-0645-41a1-b050-0c7056a9f8af', 'abc', 'abc', 123, '2020-10-01')",
            commit=True,
        )
        run_query(
            f"{insert_stmt} VALUES('xyz', 'Dillan Harrison', 'abc', 123, '2020-10-01')",
            commit=True,
        )

        # check no rows are added
        assert_row_count("users", 1000)

        # check default values
        run_query(
            "INSERT INTO users(user_id, name, password, registered_at)"
            + " VALUES('xyz', 'abc', 'abc', '2020-10-01')",
            commit=True,
        )
        res = run_query("SELECT followers FROM users WHERE user_id = 'xyz'")[0][
            "followers"
        ]
        assert_eq(res, 0, err_msg="Check default value constraint")
        assert_row_count("users", 1001)

    with Scorer(3, "Create table categories"):
        migrate.create_table_categories()
        # check existence of table categories
        check_table("categories")

    with Scorer(4, "Copy categories from PostgreSQL to SQLite"):
        migrate.copy_categories()
        check_table_content(
            "categories",
            15,
            ["ID", "Category name"],
        )

    with Scorer(4, "Check constraint on categories"):
        insert_stmt = 'INSERT INTO categories(ID, "Category Name")'
        # null values
        run_query(f"{insert_stmt} VALUES(NULL, 'abc')", commit=True)
        run_query(f"{insert_stmt} VALUES(123, NULL)", commit=True)

        # unique
        run_query(f"{insert_stmt} VALUES(1, 'abc')", commit=True)
        run_query(f"{insert_stmt} VALUES(123, 'Pets & Animals')", commit=True)

        # check no rows are added
        assert_row_count("categories", 15)

        # add valid row
        run_query(f"{insert_stmt} VALUES(1234, 'Storm')", commit=True)
        assert_row_count("categories", 16)

    with Scorer(3, "Create table videos"):
        migrate.create_table_videos()
        # check existence of table videos
        check_table("videos")

    with Scorer(5, "Copy videos from PostgreSQL to SQLite"):
        migrate.copy_videos()
        check_table_content(
            "videos",
            1000,
            ["video_id", "title", "length (min)", "category_id", "created_at"],
        )

    with Scorer(7, "Check constraint on videos"):
        insert_stmt = 'INSERT INTO videos(video_id, title, "length (min)", category_id, created_at)'
        # null values
        run_query(
            f"{insert_stmt} VALUES(NULL, 'abc', 12.3, 12, '2020-10-01')", commit=True
        )
        run_query(
            f"{insert_stmt} VALUES('abc', NULL, 12.3, 12, '2020-10-01')", commit=True
        )
        run_query(f"{insert_stmt} VALUES('abc', 'abc', 12.3, 12, NULL)", commit=True)

        # unique
        run_query(
            f"{insert_stmt} VALUES('132f767c-2507-4de8-8609-0268c7c2c651', 'abc', 12.3, 12, '2020-10-01')",
            commit=True,
        )

        # foreign keys
        run_query(f"{insert_stmt} VALUES('abc', 'abc', 12.3, 123, NULL)", commit=True)

        # check no rows are added
        assert_row_count("videos", 1000)

        # check default values
        run_query(
            "INSERT INTO videos(video_id, title, category_id, created_at)"
            + " VALUES('xyz', 'abc', 12, '2020-10-01')",
            commit=True,
        )
        res = run_query(
            "SELECT \"length (min)\" AS l FROM videos WHERE video_id = 'xyz'"
        )[0]["l"]
        assert_eq(res, 0.0, err_msg="Check default value constraint")
        assert_row_count("videos", 1001)

    with Scorer(3, "Create table views"):
        migrate.create_table_views()
        # check existence of table views
        check_table("views")

    with Scorer(5, "Copy views from PostgreSQL to SQLite"):
        migrate.copy_views()
        check_table_content(
            "views",
            20000,
            ["view_id", "user_id", "video_id", "started_at", "finished_at"],
        )

    with Scorer(6, "Check constraint on views"):
        insert_stmt = "INSERT INTO views(view_id, started_at)"
        # null values
        run_query(f"{insert_stmt} VALUES(NULL, '2020-10-01')", commit=True)
        run_query(f"{insert_stmt} VALUES('123', NULL)", commit=True)

        # unique
        run_query(
            f"{insert_stmt} VALUES('b7668e2f-127e-46b6-96ed-42df8fe2d368', '2020-10-01')",
            commit=True,
        )

        # foreign keys
        run_query(
            f"INSERT INTO views(view_id, user_id, video_id, started_at, finished_at)"
            + " VALUES('abc', 'a4ca07d3-0645-41a1-b050-0c7056a9f8ae', '132f767c-2507-4de8-8609-0268c7c2c651', '2020-01-01', NULL)",
            commit=True,
        )

        run_query(
            f"INSERT INTO views(view_id, user_id, video_id, started_at, finished_at)"
            + " VALUES('abc', 'a4ca07d3-0645-41a1-b050-0c7056a9f8af', '132f767c-2507-4de8-8609-0268c7c2c641', '2020-01-01', NULL)",
            commit=True,
        )

        # check no rows are added
        assert_row_count("views", 20000)

        # valid row
        run_query(
            f"INSERT INTO views(view_id, user_id, video_id, started_at, finished_at)"
            + " VALUES('abc', 'a4ca07d3-0645-41a1-b050-0c7056a9f8af', '132f767c-2507-4de8-8609-0268c7c2c651', '2020-01-01', NULL)",
            commit=True,
        )
        assert_row_count("views", 20001)


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Assignment 3...")
    tests = [test_explore, test_migrate]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Assignment 3:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
