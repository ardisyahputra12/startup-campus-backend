"""
Divide it whole. [WEIGHT = 1]

Given two non-negative integers a and b, find the result of dividing a with b but with some notes:
- If the result is not an integer, return the result rounded down to the nearest integer.
- If b equals 0, return -1

Examples
------------------------------------
Input: a = 13, b = 3
Output: 4
Explanation: 13/3 = 4.3333.., rounded down to 4
------------------------------------
Input: a = 4, b = 9
Output: 0
Explanation: 4/9 = 0.444.., rounded down to 0
------------------------------------
Input: a = 7, b = 0
Output: -1
------------------------------------
"""


def divide_whole(a: int, b: int) -> int:
    if b == 0: return -1
    else: return a//b


# print(divide_whole(13, 3))
# print(divide_whole(4, 9))
# print(divide_whole(7, 0))