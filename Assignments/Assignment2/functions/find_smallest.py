def f1(l: list):
    return min(l)


def f2(l: list):
    res = min([e for e in l if e >= 0])
    if res >= 0:
        return res

    return -1


def f3(l: list):
    # find 1st positive integer in the list
    result = None
    for e in l:
        if e <= 0:
            continue
        if result is None:
            result = e
        elif e < result:
            result = e

    return result
