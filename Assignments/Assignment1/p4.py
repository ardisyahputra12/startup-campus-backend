"""
Arithmetic generator. [WEIGHT = 1]

Given 3 inputs:
- a (type: integer)
- b (type: integer, 0 < amount <= 100)
- diff (type: integer)

Generate b numbers, starting from a. Each subsequent number must have difference of diff.
When diff is a negative number, the next number should be less than previous number.

Return the numbers as a list.

Examples
------------------------------------
Input: a = 3, b = 5, diff = 4
Output: [3, 7, 11, 15, 19]
Explanation: First number is 3, then generate 4 (y-1) next numbers with difference of +4
------------------------------------
Input: a = 6, b = 4  diff = -2
Output: [6, 4, 2, 0]
Explanation: Starts at 6, minus 2 until we generate 4 numbers
------------------------------------
"""


def arithmetic_generator(a: int, b: int, diff: int) -> list:
    val = []
    while True:
        val.append(a)
        a += diff
        if len(val) == b: break
    return val


# print(arithmetic_generator(3, 5, 4))
# print(arithmetic_generator(6, 4, -2))