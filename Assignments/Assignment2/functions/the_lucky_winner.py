def the_lucky_winner(names, lottery_numbers, N):
    # prevent you from inputting invalid entries
    validate(names, lottery_numbers, N)

    # check for unique individuals
    if contains_duplicate(names):
        return "Found duplicate participants"

    # check for unique lottery number
    if contains_duplicate(lottery_numbers):
        return "Found duplicate numbers"

    number_to_person = dict(zip(lottery_numbers, names))
    while N > 0:
        if N in number_to_person:
            return number_to_person[N]
        N //= 2

    return "No winner this time"


def f1(names, lottery_numbers, N):
    # check for unique lottery number
    if contains_duplicate(lottery_numbers):
        return "Found duplicate numbers"

    number_to_person = dict(zip(lottery_numbers, names))
    while N > 0:
        if N in number_to_person:
            return number_to_person[N]
        N //= 2

    return "No winner this time"


def f2(names, lottery_numbers, N):
    # check for unique individuals
    if contains_duplicate(names):
        return "Found duplicate participants"

    number_to_person = dict(zip(lottery_numbers, names))
    while N > 0:
        if N in number_to_person:
            return number_to_person[N]
        N //= 2

    return "No winner this time"


def f3(names, lottery_numbers, N):
    # check for unique individuals
    if contains_duplicate(names):
        return "Found duplicate participants"

    # check for unique lottery number
    if contains_duplicate(lottery_numbers):
        return "Found duplicate numbers"

    number_to_person = dict(zip(lottery_numbers, names))
    while N > 0:
        if N in number_to_person:
            return number_to_person[N]
        N //= 2


def f4(names, lottery_numbers, N):
    # check for unique individuals
    if contains_duplicate(names):
        return "Found duplicate participants"

    # check for unique lottery number
    if contains_duplicate(lottery_numbers):
        return "Found duplicate numbers"

    number_to_person = dict(zip(lottery_numbers, names))
    while N > 1:
        if N in number_to_person:
            return number_to_person[N]
        N //= 2

    return "No winner this time"


def validate(names, lottery_numbers, N):
    assert isinstance(names, list)
    assert isinstance(lottery_numbers, list)
    assert N > 0, "N must be positive"

    for name in names:
        assert isinstance(name, str)
    for number in lottery_numbers:
        assert isinstance(number, int)
        assert number >= 1, "Lottery number can't be smaller than 1"
        assert number <= 1000, "Lottery number can't be bigger than 1000"


def contains_duplicate(l) -> bool:
    unique_objects = set(l)
    return len(unique_objects) != len(l)
