"""
Even sum. [WEIGHT = 1]

Given a list of integers, return the sum of the even numbers within a list. 
If the list doesn't contain any even numbers, return 0. The list will contain
at most 1000 integers between -1000 and 1000 (inclusive).

Examples
------------------------------------
Input: [0, 2, 3, 4]
Output: 6
Explanation: All numbers are even except 3, so the total is 0+2+4 = 6
------------------------------------
Input: [-11, 3, 7]
Output: 0
Explanation: All numbers are odd, so return 0
------------------------------------

"""


def even_sum(l: list):
    val = 0
    for i in l:
        if i%2 == 0: val += i
    return val


# print(even_sum([0, 2, 3, 4]))
# print(even_sum([-11, 3, 7]))