from functools import wraps
from json import dumps
from typing import List, Union

FAILED_CASES = []


def score_case(d: dict) -> Union[int, int]:
    qs = d.get("query", [])
    outs = d.get("output", [])
    weights = d.get("weight", [])

    total_score = 0
    total_weights = sum(weights)

    for q, out, weight in zip(qs, outs, weights):
        try:
            res = eval(q)
            if res == out:
                total_score += weight
            else:
                FAILED_CASES.append({"query": q, "exp": out, "output": res})
        except Exception as exc:
            FAILED_CASES.append({"query": q, "exp": out, "exc": str(exc)})

    return total_score, total_weights


def grade(title: str):
    def dec(f: callable):
        @wraps(f)
        def dec2(*args, **kwargs):
            print(f"Grading {title}...")
            total_score, total_weights = f(*args, **kwargs)

            print(
                f"Your score for {title}: {total_score} out of {total_weights}",
                end="\n\n",
            )

            return total_score, total_weights

        return dec2

    return dec


def score_cases(cases: List[dict], inputs: List) -> Union[int, int]:
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
        print("You failed some test cases")
        var_name, class_name, args_d = inputs
        print("Input")
        for index, v in enumerate(args_d):
            args = [dumps(e) for e in v.get("args", [])]
            kwargs = [f"{k1}={dumps(v1)}" for k1, v1 in v.get("kwargs", {}).items()]
            all_args = args + kwargs
            print(f"  {var_name}[{index}] = {class_name}({', '.join(all_args)})")
        print()

    for case in FAILED_CASES:
        q = case["query"]
        print(f"  You failed this test case: {q}")
        exp_output = case["exp"]
        exc = case.get("exc")

        print("  Your Output: ", end="")
        if exc:
            print(f"RUNTIME ERROR: {exc}")
        else:
            user_output = case["output"]
            print(user_output)
        print(f"  Expected Output; {exp_output}", end="\n\n")

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

    all_args = [
        {"args": ("Charlie", "cat"), "kwargs": {"birth_year": 2003}},
        {"args": ("Dante", "dog"), "kwargs": {"birth_year": 2005}},
        {"args": ("Simba", "cat"), "kwargs": {}},
        {"args": ("Robin", "bird"), "kwargs": {"birth_year": 2010}},
        {"args": ("Joy", "dog"), "kwargs": {}},
    ]
    global pets
    pets = [get_object(Pet, arg) for arg in all_args]
    inputs = ["pets", "Pet", all_args]
    cases = [
        {
            "query": [
                "pets[0].name",
                "pets[1].type",
                "pets[1].age(2010)",
                "pets[2].same_type(pets[0])",
                "pets[2].age(2022)",
                "pets[1].same_type(pets[2])",
            ],
            "output": ["Charlie", "dog", 5, True, 2, False],
            "weight": [1, 1, 1, 1, 1, 1],
        },
        {
            "query": [
                "pets[3].name",
                "pets[4].type",
                "pets[4].age(2022)",
                "pets[3].age(2013)",
                "pets[3].same_type(pets[2])",
                "pets[1].same_type(pets[4])",
            ],
            "output": ["Robin", "dog", 2, 3, False, True],
            "weight": [1, 1, 1, 1, 1, 1],
        },
        # edge cases
        {
            "query": [
                "pets[3].same_type(pets[3])",
                "pets[1].age(2005)",
                "pets[2].age(2019)",
            ],
            "output": [True, 0, "Not applicable"],
            "weight": [1, 1, 1],
        },
    ]

    return score_cases(cases, inputs)


##############################################################################################

if __name__ == "__main__":
    tests = [test_p1]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    print(f"Your grade for Assignment 2 is {final_score}/{perfect_score} ({perc}%)")
