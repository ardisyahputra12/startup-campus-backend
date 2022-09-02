def f1(l: list):
    try:
        return min(l)
    except:
        return -1


def f2(l: list):
    try:
        res = min([e for e in l if e >= 0])
        if res >= 0:
            return res
    finally:
        return -1


def f3(l: list):
    # find 1st positive integer in the list
    result = None
    for e in l:
        if result is None:
            result = e

        if e <= 0:
            continue
        elif e < result:
            result = e

    return result if result > 0 else -1
