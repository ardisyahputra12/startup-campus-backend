# DO NOT EDIT THIS FILE

from functools import wraps
from json import dumps, loads
from typing import List, Union
from unittest.mock import patch

FAILED_CASES = []


def score_case(d: dict) -> Union[int, int]:
    raw_input = d.get("input", [])
    input = [eval(e) for e in raw_input]  # noqa
    qs = d.get("query", [])
    outs = d.get("output", [])
    weights = d.get("weight", [])

    total_score = 0
    total_weights = sum(weights)

    for q, out, weight in zip(qs, outs, weights):
        case = {"input": raw_input, "query": q, "exp": out}
        try:
            res = eval(q)
            if res == out:
                total_score += weight
            else:
                FAILED_CASES.append({**case, "output": res})
        except Exception as exc:
            FAILED_CASES.append({**case, "exc": str(exc)})

    return total_score, total_weights


def grade(title: str):
    def dec(f: callable):
        @wraps(f)
        def dec2(*args, **kwargs):
            print("=" * 100)
            print(f"Grading {title}...")
            total_score, total_weights = f(*args, **kwargs)

            print(f"\nYour score for {title}: {total_score} out of {total_weights}")

            return total_score, total_weights

        return dec2

    return dec


def score_cases(cases: List[dict]) -> Union[int, int]:
    total_score = 0
    total_weight = 0

    # summarize scores
    for case in cases:
        score, weight = score_case(case)
        total_score += score
        total_weight += weight

    # print failed cases
    global FAILED_CASES
    if FAILED_CASES:
        print("  Displaying several failed cases...\n")
        # only display first 3 failed cases
        for case in FAILED_CASES[:3]:
            print("  Input:")
            input = case["input"]
            for i, e in enumerate(input):
                print(f"    input[{i}]: {e}")
            print()

            q = case["query"]
            print(f"  You failed this test case: {q}")
            exp_output = case["exp"]
            print("    Your Output: ", end="")
            exc = case.get("exc")

            if exc:
                print(f"RUNTIME ERROR: {exc}")
            else:
                user_output = case["output"]
                print(user_output)
            print(f"    Expected Output: {exp_output}")
            print("-" * 100)

    # reset to None
    FAILED_CASES = []

    return total_score, total_weight


def get_object(cls, arg_d: dict):
    args = arg_d.get("args", [])
    kwargs = arg_d.get("kwargs", {})
    return cls(*args, **kwargs)


##############################################################################################


@grade("Problem 1")
def test_p1():
    from p1 import Pet

    global Pet

    cases = [
        {
            "input": [
                'Pet("Charlie", "cat", birth_year=2003)',
                'Pet("Dante", "dog", birth_year=2005)',
                'Pet("Simba", "cat")',
            ],
            "query": [
                "input[0].name",
                "input[1].type",
                "input[1].age(2010)",
                "input[2].same_type(input[0])",
                "input[2].age(2022)",
                "input[1].same_type(input[2])",
            ],
            "output": ["Charlie", "dog", 5, True, 2, False],
            "weight": [1, 1, 1, 1, 1, 1],
        },
        {
            "input": [
                'Pet("Dante", "dog", birth_year=2005)',
                'Pet("Simba", "cat")',
                'Pet("Robin", "bird", birth_year=2010)',
                'Pet("Joy", "dog")',
            ],
            "query": [
                "input[2].name",
                "input[3].type",
                "input[3].age(2022)",
                "input[2].age(2013)",
                "input[2].same_type(input[1])",
                "input[0].same_type(input[3])",
            ],
            "output": ["Robin", "dog", 2, 3, False, True],
            "weight": [1, 1, 1, 1, 1, 1],
        },
        # edge cases
        {
            "input": [
                'Pet("Dante", "dog", birth_year=2005)',
                'Pet("Simba", "cat")',
                'Pet("Robin", "bird", birth_year=2010)',
            ],
            "query": [
                "input[2].same_type(input[2])",
                "input[0].age(2005)",
                "input[1].age(2019)",
            ],
            "output": [True, 0, "Not applicable"],
            "weight": [1, 1, 1],
        },
    ]

    return score_cases(cases)


@grade("Problem 2")
def test_p2():
    from p2 import Student

    global Student

    cases = [
        {
            "input": [
                'Student("Adam", "Smith", grades=[90, 80])',
                'Student("Bryant", "Lenin", grades=[70, 65.3])',
                'Student("Claire", "Voy", grades=[72.8, 97.2])',
            ],
            "query": [
                "str(input[0])",
                "input[0] < input[1]",
                "input[0] <= input[2]",
                "str(input[1])",
                "str(input[2])",
                "input[0].highest_score()",
                "input[2].lowest_score()",
                "input[2] > input[0]",
            ],
            "output": [
                "[Adam Smith] - score: 170",
                False,
                True,
                "[Bryant Lenin] - score: 136",
                "[Claire Voy] - score: 170",
                90,
                72.8,
                False,
            ],
            "weight": [1, 1, 1, 1, 1, 1, 1, 1],
        },
        # edge cases
        {
            "input": [
                'Student("Zero", "Void", grades=[])',
                'Student("Mira", "Twin", grades=[64, 86, 78])',
                'Student("Prabu", "Twin", grades=[73.8, 87.79, 66.5])',
            ],
            "query": [
                "str(input[0])",
                "input[1].lowest_score()",
                "input[1] > input[0]",
                "input[2] != input[0]",
                "input[0].highest_score()",
                "str(input[2])",
                "input[0].lowest_score()",
            ],
            "output": [
                "[Zero Void] - score: 0",
                64,
                True,
                True,
                0,
                "[Prabu Twin] - score: 229",
                0,
            ],
            "weight": [1, 1, 1, 1, 1, 1, 1],
        },
    ]

    return score_cases(cases)


@grade("Problem 3")
def test_p3():
    from p3 import Motorbike, Sedan, Truck, cheapest_ride

    global Motorbike, Sedan, Truck, cheapest_ride

    cases = [
        {
            "input": [
                'Motorbike("M1", 40)',
                'Sedan("Ruby", 200)',
                'Truck("Kargo", 2000)',
            ],
            "query": [
                "cheapest_ride(input, distance=100, load=100, time_limit=2)",
                "cheapest_ride(input, distance=100, load=180, time_limit=3)",
                "cheapest_ride(input, distance=10, load=5, time_limit=0.5)",
                "cheapest_ride(input, distance=10, load=5, time_limit=0.1)",
            ],
            "output": ["Ruby", "Ruby", "M1", "Impossible"],
            "weight": [1, 1, 1, 1],
        },
        {
            "input": [
                'Motorbike("M1", 40)',
                'Motorbike("M2", 60)',
                'Motorbike("M3", 100)',
                'Sedan("Mini", 100)',
                'Sedan("Ruby", 200)',
                'Sedan("Gianto", 600)',
                'Truck("Tiny", 600)',
                'Truck("Kargo", 2000)',
            ],
            "query": [
                "cheapest_ride(input, distance=101, load=2000, time_limit=4)",
                "cheapest_ride(input, distance=100, load=2000, time_limit=4)",
                "cheapest_ride(input, distance=78, load=600, time_limit=2)",
                "cheapest_ride(input, distance=80, load=500, time_limit=2)",
                "cheapest_ride(input, distance=104, load=200, time_limit=2)",
                "cheapest_ride(input, distance=104, load=200, time_limit=1.9)",
                "cheapest_ride(input, distance=112, load=100, time_limit=1.99)",
                "cheapest_ride(input, distance=88, load=100, time_limit=1.99)",
                "cheapest_ride(input, distance=88, load=100, time_limit=2)",
                "cheapest_ride(input, distance=80, load=100, time_limit=1.99)",
                "cheapest_ride(input, distance=80, load=100, time_limit=2)",
                "cheapest_ride(input, distance=80, load=100, time_limit=2)",
            ],
            "output": [
                "Impossible",
                "Kargo",
                "Kargo",
                "Gianto",
                "Gianto",
                "Impossible",
                "Impossible",
                "Gianto",
                "Gianto",
                "Gianto",
                "M3",
            ],
            "weight": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        },
        {
            "input": [
                'Motorbike("Rouge", 100)',
                'Sedan("Bellamy", 80)',
                'Truck("Dragon", 1000)',
            ],
            "query": [
                "cheapest_ride(input, distance=45, load=100, time_limit=1)",
                "cheapest_ride(input, distance=40, load=100, time_limit=0.99)",
                "cheapest_ride(input, distance=40, load=100, time_limit=1)",
                "cheapest_ride(input, distance=57, load=80, time_limit=1.2)",
                "cheapest_ride(input, distance=0, load=1001, time_limit=1)",
            ],
            "output": ["Impossible", "Dragon", "Rouge", "Bellamy", "Impossible"],
            "weight": [1, 1, 1, 1, 1],
        },
    ]

    return score_cases(cases)


@grade("Problem 4")
def test_p4():
    from functions.find_smallest import f1, f2, f3
    from p4 import FindSmallestTest, find_smallest

    total_scores = 0
    total_weights = 15

    # 1 pt per case (max: 5 PTS)
    cases = set(
        [dumps(case) for case in FindSmallestTest.cases if isinstance(case["l"], list)]
    )
    case_len = len(cases)
    inc = min(case_len, 5)
    print(f"  {case_len} valid, UNIQUE test case(s) found: {inc} pts")
    total_scores += inc
    # return to original
    cases = [loads(case) for case in cases]

    # positive testing (max: 4 PTS)
    print("  [Positive Testing]")
    valid_cases = 0
    for index, case in enumerate(cases, 1):
        try:
            assert find_smallest(case["l"]) == case["expected"]
            valid_cases += 1
        except Exception:
            print(f"    Fails test for case #{index}")
            pass
    tmp = 4 * valid_cases / case_len if case_len else 0
    print(f"  {valid_cases}/{case_len} cases are valid: {tmp} pts")
    total_scores += tmp

    # negative testing (max: 6 PTS)
    print("  [Negative Testing]")
    tmp = 0
    false_functions = (f1, f2, f3)
    for index, f in enumerate(false_functions):
        with patch("p4.find_smallest", f):
            found_fail_assertions = False
            try:
                FindSmallestTest().test_valid()
            except Exception as e:
                if isinstance(e, AssertionError):
                    found_fail_assertions = True
                    tmp += 1
            finally:
                if not found_fail_assertions:
                    print(f"    Fail to cover false implementation #{index+1}")
    print(f"    Your test cases cover {tmp} false implementation(s): {tmp*2} pts")
    total_scores += 2 * tmp

    return total_scores, total_weights


@grade("Problem 5")
def test_p5():
    from functions.the_lucky_winner import f1, f2, f3, f4
    from p5 import LuckyWinnerTest

    total_scores = 0
    total_weights = 15

    # positive testing
    print("  [Positive Testing]")
    try:
        LuckyWinnerTest().test_valid()
        total_scores += 3
        print("    Passed all assertions for the correct implementation (3 pts)")
    except Exception as e:
        print(
            f"    Some of your test cases fail to test the correct implementation: {e}"
        )

    # negative testing (max: 12 PTS)
    if total_scores > 0:
        print("  [Negative Testing]")
        tmp = 0
        false_functions = (f1, f2, f3, f4)
        for index, f in enumerate(false_functions):
            with patch("p5.the_lucky_winner", f):
                found_fail_assertions = False
                try:
                    LuckyWinnerTest().test_valid()
                except Exception as e:
                    if isinstance(e, AssertionError):
                        found_fail_assertions = True
                        tmp += 1
                finally:
                    if not found_fail_assertions:
                        print(f"    Fail to cover false implementation #{index+1}")
        print(f"    Your test cases cover {tmp} false implementation(s): {tmp*3} pts")
        total_scores += tmp * 3
    else:
        print(
            f"\n  Skip checking false implementations, please make sure your test cases"
            " cover the correct implementation (Positive Testing)"
        )

    return total_scores, total_weights


# @grade("Problem 6")
# def test_p6():
#     return 0, 25


##############################################################################################

if __name__ == "__main__":
    tests = [test_p1, test_p2, test_p3, test_p4, test_p5]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    print("=" * 100 + "\n")
    print(f"YOUR GRADE FOR ASSIGNMENT 2: {final_score}/{perfect_score} ({perc}%)\n")
    print("=" * 100)
