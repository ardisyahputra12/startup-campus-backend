from json import dumps
from typing import List

FAILED_CASE = None


def score_case(f: callable, input_d: dict) -> bool:
    args = input_d.get("args", [])
    kwargs = input_d.get("kwargs", {})
    exp_output = input_d["result"]

    try:
        user_output = f(*args, **kwargs)
        assert f(*args, **kwargs) == exp_output
        return True
    except Exception as exc:
        global FAILED_CASE
        if not FAILED_CASE:
            if str(exc):
                user_output = None
            FAILED_CASE = f, args, kwargs, user_output, exp_output, str(exc)
        return False


def grade(title: str, weight: str):
    def dec(f: callable):
        def dec2(*args, **kwargs):
            print(f"Grading {title} (weight=1)... ")
            user_score, full_score = f(*args, **kwargs)

            print(f"    You solved {user_score} out of {full_score} cases", end=" ")
            print(f"[SCORE:{user_score * weight}]\n")

            return user_score * weight, full_score * weight

        return dec2

    return dec


def stringify(v):
    return dumps(v)


def process_case(f: callable, cases: List[dict]):
    res = sum([score_case(f, case) for case in cases])

    global FAILED_CASE
    if FAILED_CASE:
        f, args, kwargs, user_output, exp_output, exc = FAILED_CASE
        print("    You failed this test case: ", end="")
        final_args = [stringify(e) for e in args] + [
            f"{stringify(k)}={stringify(v)}" for k, v in kwargs.items()
        ]
        print("{}({})".format(f.__name__, ",".join(final_args)))

        spaces = " " * 8
        if str(exc):
            print("{}YOUR OUTPUT > {}".format(spaces, f"RUNTIME ERROR: {exc}"))
        else:
            print("{}YOUR OUTPUT > {}".format(spaces, stringify(user_output)))
        print("{}SHOULD BE > {}".format(spaces, stringify(exp_output)))

        # reset to None
        FAILED_CASE = None

    return res, len(cases)


@grade("Problem 1", weight=1)
def test_p1():
    from p1 import divide_whole

    cases = [
        {"args": (13, 3), "result": 4},
        {"args": (4, 9), "result": 0},
        {"args": (7, 0), "result": -1},
        {"args": (56088, 123), "result": 456},
        {"args": (0, 0), "result": -1},
        {"args": (0, 0), "result": -1},
    ]

    return process_case(divide_whole, cases)


@grade("Problem 2", weight=1)
def test_p2():
    from p2 import clean_sentence

    cases = [
        {"args": ("I am learning Python3???",), "result": "I am learning Python3"},
        {"args": {"Everything is good"}, "result": "Everything is good"},
        {
            "args": {"  Independence day:August 17th,1945 "},
            "result": "Independence day August 17th 1945",
        },
        {
            "args": {"There are~2 rabbits|3 dogs_10 cats?in-my+house"},
            "result": "There are 2 rabbits 3 dogs 10 cats in my house",
        },
        {
            "args": {"None of these should be allowed!@#$%^&*()"},
            "result": "None of these should be allowed",
        },
        {
            "args": {"Spaces in the mid     dle are fine but this is not    "},
            "result": "Spaces in the mid     dle are fine but this is not",
        },
    ]

    return process_case(clean_sentence, cases)


@grade("Problem 3", weight=1)
def test_p3():
    from p3 import even_sum

    cases = [
        {"args": ([0, 2, 3, 4],), "result": 6},
        {"args": ([-11, 3, 7],), "result": 0},
        {"args": ([-80, 83, 46, -97, -21],), "result": -34},
        {
            "args": ([675, -231, 912, 260, 538, 562, -505, -264, 463, 973],),
            "result": 2008,
        },
        {"args": ([i for i in range(1000) if i % 2 != 0],), "result": 0},
        {"args": ([],), "result": 0},
    ]

    return process_case(even_sum, cases)


if __name__ == "__main__":
    tests = [test_p1, test_p2, test_p3]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        user_score, full_score = test_f()
        final_score += user_score
        perfect_score += full_score

    perc = round(final_score / perfect_score * 100, 1)
    print(f"Your grade for Assignment #1 is {final_score}/{perfect_score} ({perc}%)")
