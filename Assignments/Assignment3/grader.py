"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
from functools import wraps
from io import StringIO
from unittest.mock import patch

import explore
import migrate

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


def assert_eq(expression, expected, exc_type=AssertionError):
    try:
        if expression == expected:
            return
        else:
            err = "\n".join([f"Expected: {expected}", f"Yours: {expression}"])
            raise exc_type(err)
    except Exception:
        raise


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
    with Scorer(1, "Exploring"):
        pass

    # with Scorer(2, "Checking initial buyers/sellers"):
    #     assert_eq(my_shop.sellers, [])
    #     assert_eq(my_shop.buyers, [])

    # # register 2 seller and 3 buyers (2 pts each for seller/buyer)
    # with Scorer(1, "Registering valid sellers"):
    #     seller1 = Seller("Robert", my_shop)
    #     seller2 = Seller("Dwight", my_shop)
    # with Scorer(1, "Registering valid buyers"):
    #     buyer1 = Buyer("Bob", my_shop)
    #     buyer2 = Buyer("Alice", my_shop)
    #     buyer3 = Buyer("Charlie", my_shop)

    # # check printed statement when registering with existing username (2 pts each)
    # with Scorer(1, "Registering illegal seller"):
    #     with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
    #         illegal_seller = Seller("Dwight", my_shop)
    #     assert_eq(
    #         mock_stdout.getvalue()[:-1],
    #         "Dwight is already a registered seller",
    #         exc_type=DisplayError,
    #     )
    # with Scorer(1, "Registering illegal buyer"):
    #     with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
    #         illegal_buyer = Buyer("Charlie", my_shop)
    #     assert_eq(
    #         mock_stdout.getvalue()[:-1],
    #         "Charlie is already a registered buyer",
    #         exc_type=DisplayError,
    #     )

    # # check list of sellers/buyers (2 pts each)
    # with Scorer(2, "Checking registered sellers"):
    #     assert_eq(my_shop.sellers, ["Dwight", "Robert"])
    # with Scorer(2, "Checking registered buyers"):
    #     assert_eq(my_shop.buyers, ["Alice", "Bob", "Charlie"])


@grade
def test_migrate():
    with Scorer(1, "Exploring"):
        pass


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
