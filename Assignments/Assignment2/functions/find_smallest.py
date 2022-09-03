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
    try:
        result = l[0]
        for e in l[1:]:
            if e <= 0:
                continue
            elif result < 0 or e < result:
                result = e

        return result if result > 0 else -1
    except Exception:
        return 0
