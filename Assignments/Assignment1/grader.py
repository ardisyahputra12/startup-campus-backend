from functools import wraps
from json import dumps
from random import choices, randint
from string import ascii_lowercase
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
        @wraps(f)
        def dec2(*args, **kwargs):
            print(f"Grading {title} (weight={weight})... ")
            user_score, full_score = f(*args, **kwargs)

            print(f"    You solved {user_score} out of {full_score} cases", end=" ")
            print(f"[SCORE:{user_score * weight}]\n")

            return user_score * weight, full_score * weight

        return dec2

    return dec


def stringify(v):
    try:
        return dumps(v)
    except TypeError:
        return str(v)


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
        {"args": (888, 321), "result": 2},
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
        {"args": {"???Vini\nVidi\nVici!\n"}, "result": "Vini Vidi Vici"},
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


@grade("Problem 4", weight=1)
def test_p4():
    from p4 import arithmetic_generator

    cases = [
        {"args": (3, 5, 4), "result": [3, 7, 11, 15, 19]},
        {"args": (6, 4, -2), "result": [6, 4, 2, 0]},
        {"args": (9, 10, 12), "result": [9, 21, 33, 45, 57, 69, 81, 93, 105, 117]},
        {
            "args": (1, 20, 0),
            "result": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        },
        {
            "args": (0, 10, -13),
            "result": [0, -13, -26, -39, -52, -65, -78, -91, -104, -117],
        },
        {"args": (123456789, 1, 1000), "result": [123456789]},
    ]
    return process_case(arithmetic_generator, cases)


@grade("Problem 5", weight=1)
def test_p5():
    from p5 import find_by_label

    cases = [
        {
            "args": (
                ["club_name", "score", "captain"],
                ["manchester united", "4-0", "maguire"],
                "score",
            ),
            "result": "4-0",
        },
        {
            "args": (
                ["name", "age", "birthday"],
                ["jhony", 21, "August 14, 1995"],
                "score",
            ),
            "result": "Information not available",
        },
        {
            "args": (
                ["name", "age", "birthday"],
                ["jhony", 21, "August 14, 1995"],
                "name",
            ),
            "result": "jhony",
        },
        {
            "args": (["index", "title", "extra"], [0, "Mr.", ["a", "b"]], "extra"),
            "result": ["a", "b"],
        },
        {
            "args": (["index", "title", "extra"], [0, "Mr.", None], "Index"),
            "result": "Information not available",
        },
    ]
    return process_case(find_by_label, cases)


@grade("Problem 6", weight=1)
def test_p6():
    from p6 import factorial

    cases = [
        {"args": (5,), "result": 120},
        {"args": (10,), "result": 3628800},
        {"args": (7,), "result": 5040},
        {"args": (20,), "result": 2432902008176640000},
        {"args": (-7,), "result": -1},
        {"args": (0,), "result": 1},
        {"args": (1,), "result": 1},
    ]
    return process_case(factorial, cases)


@grade("Problem 7", weight=2)
def test_p7():
    from p7 import smartest_students

    all_except_A = [chr(ord("Z") - i) for i in range(25)]
    cases = [
        {"args": ({"Alan": 80, "Bishop": 90, "Claire": 80},), "result": "Bishop"},
        {
            "args": ({"Dwight": 80, "Bishop": 70, "Claire": 80},),
            "result": ["Claire", "Dwight"],
        },
        {
            "args": ({"Alan": 85, "Bishop": 85},),
            "result": "All are winners",
        },
        {
            "args": (
                {
                    **{
                        "".join(choices(ascii_lowercase, k=5)).capitalize(): randint(
                            1, 99
                        )
                        for _ in range(98)
                    },
                    "Aa": 100,
                    "A": 100,
                },
            ),
            "result": ["A", "Aa"],
        },
        {
            "args": ({"A": 99, **{c: 100 for c in all_except_A}},),
            "result": sorted(all_except_A),
        },
        {
            "args": ({"Alan J": 75, "Alan X": 70, "Alan B": 75},),
            "result": ["Alan B", "Alan J"],
        },
        {"args": ({"Alone": 93},), "result": "All are winners"},
    ]

    return process_case(smartest_students, cases)


@grade("Problem 8", weight=2)
def test_p8():
    from p8 import calculate_through_commands

    cases = [
        {"args": (8, ["mul 2", "sub 4"]), "result": 12},
        {"args": (2, ["add 3", "reset", "sub 2"]), "result": 0},
        {"args": (-10, ["mul -3", "stop", "sub 2", "add -5"]), "result": 30},
        {
            "args": (
                0,
                ["reset", "sub 8", "sub -2", "stop", "sub 2", "mul -9", "sub -9"],
            ),
            "result": -6,
        },
        {
            "args": (
                1000,
                [
                    "reset",
                    "reset",
                    "reset",
                    "add -4",
                    "add 6",
                    "reset",
                    "add -6",
                    "add -9",
                    "sub 5",
                    "add 7",
                ],
            ),
            "result": 987,
        },
        {
            "args": (
                -1000,
                [
                    "sub -9",
                    "sub -1",
                    "add -7",
                    "sub 7",
                    "mul -5",
                    "stop",
                    "add 0",
                    "mul -7",
                    "add -8",
                    "stop",
                ],
            ),
            "result": 5020,
        },
        {"args": (123, []), "result": 123},
    ]

    return process_case(calculate_through_commands, cases)


@grade("Problem 9", weight=2)
def test_p9():
    from p9 import kth_place

    cases = [
        {"args": ([3, 10, 12, 4, 5, 10], 3), "result": 5},
        {"args": ([12, 50, 30], 4), "result": "There are less than 4 unique values"},
        {"args": ([120, 100] + [randint(1, 99) for _ in range(98)], 2), "result": 100},
        {
            "args": ([-100 for _ in range(100)], 2),
            "result": "There are less than 2 unique values",
        },
        {
            "args": ([-100 for _ in range(100)], 1),
            "result": -100,
        },
        {
            "args": ([randint(1, 10) for _ in range(100)], 11),
            "result": "There are less than 11 unique values",
        },
        {
            "args": ([randint(-5, 5) for _ in range(100)], 4),
            "result": 2,
        },
    ]

    return process_case(kth_place, cases)


@grade("Problem 10", weight=3)
def test_p10():
    from p10 import summarize_subject_scores

    data1 = [
        {"name": "Santi", "science": 60, "math": 90, "computer": 100},
        {"name": "Joko", "science": 50, "math": 90, "computer": 30},
        {"name": "Budi", "science": 80, "math": 30, "computer": 30},
        {"name": "Beri", "science": 40, "math": 80, "computer": 60},
    ]
    data2 = [
        {"name": "A", "science": 80, "math": 88, "computer": 62},
        {"name": "B", "science": 89, "math": 77, "computer": 65},
        {"name": "C", "science": 89, "math": 90, "computer": 81},
        {"name": "D", "science": 82, "math": 80, "computer": 66},
        {"name": "E", "science": 85, "math": 84, "computer": 94},
        {"name": "F", "science": 81, "math": 76, "computer": 64},
        {"name": "G", "science": 88, "math": 89, "computer": 66},
        {"name": "H", "science": 83, "math": 80, "computer": 82},
        {"name": "I", "science": 87, "math": 82, "computer": 89},
        {"name": "J", "science": 88, "math": 76, "computer": 96},
        {"name": "K", "science": 80, "math": 75, "computer": 91},
        {"name": "L", "science": 85, "math": 89, "computer": 77},
        {"name": "M", "science": 82, "math": 84, "computer": 42},
        {"name": "N", "science": 81, "math": 82, "computer": 51},
        {"name": "O", "science": 84, "math": 82, "computer": 63},
        {"name": "P", "science": 89, "math": 73, "computer": 96},
        {"name": "Q", "science": 89, "math": 74, "computer": 89},
        {"name": "R", "science": 90, "math": 84, "computer": 39},
        {"name": "S", "science": 85, "math": 85, "computer": 95},
        {"name": "T", "science": 90, "math": 84, "computer": 79},
        {"name": "U", "science": 87, "math": 75, "computer": 59},
        {"name": "V", "science": 86, "math": 88, "computer": 87},
        {"name": "W", "science": 88, "math": 90, "computer": 58},
        {"name": "X", "science": 80, "math": 76, "computer": 59},
        {"name": "Y", "science": 81, "math": 73, "computer": 97},
        {"name": "Z", "science": 90, "math": 78, "computer": 71},
    ]
    cases = [
        {
            "args": (data1, "science"),
            "result": {
                "average": 58,
                "highest": {"score": 80, "names": ["Budi"]},
                "lowest": {"score": 40, "names": ["Beri"]},
            },
        },
        {
            "args": (data1, "math"),
            "result": {
                "average": 73,
                "highest": {"score": 90, "names": ["Joko", "Santi"]},
                "lowest": {"score": 30, "names": ["Budi"]},
            },
        },
        {
            "args": (data1, "computer"),
            "result": {
                "average": 55,
                "highest": {"score": 100, "names": ["Santi"]},
                "lowest": {"score": 30, "names": ["Budi", "Joko"]},
            },
        },
        {
            "args": (data2, "science"),
            "result": {
                "average": 86,
                "highest": {"score": 90, "names": ["R", "T", "Z"]},
                "lowest": {"score": 80, "names": ["A", "K", "X"]},
            },
        },
        {
            "args": (data2, "math"),
            "result": {
                "average": 82,
                "highest": {"score": 90, "names": ["C", "W"]},
                "lowest": {"score": 73, "names": ["P", "Y"]},
            },
        },
        {
            "args": (data2, "computer"),
            "result": {
                "average": 74,
                "highest": {"score": 97, "names": ["Y"]},
                "lowest": {"score": 39, "names": ["R"]},
            },
        },
        {
            "args": ([], "math"),
            "result": {
                "average": 0,
                "highest": {"score": 0, "names": []},
                "lowest": {"score": 0, "names": []},
            },
        },
    ]

    return process_case(summarize_subject_scores, cases)


if __name__ == "__main__":
    tests = [
        test_p1,
        test_p2,
        test_p3,
        test_p4,
        test_p5,
        test_p6,
        test_p7,
        test_p8,
        test_p9,
        test_p10,
    ]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        user_score, full_score = test_f()
        final_score += user_score
        perfect_score += full_score

    perc = round(final_score / perfect_score * 100, 1)
    print(f"Your grade for Assignment #1 is {final_score}/{perfect_score} ({perc}%)")
