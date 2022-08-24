"""
The kth place. [WEIGHT = 2]

Given 2 inputs, a non-empty list of integers li and a positive integer k. 

You should find the kth biggest value in li. Duplicate values in the list are considered
1 value for the sake of comparison.

If k is bigger than the number of unique values in li, you should return this message:
"There are less than k unique values"

Length of li <= 100.

Examples
------------------------------------
Input: li = [3,10,12,4,5,10], k = 3
Output: 5
Explanation: When ordering li from the biggest value, we get:
- 12 -> greatest value
- 10 (2 occurrences) -> treat as 1 value, 2nd greatest
- 5 -> 3rd greatest
------------------------------------
Input: li = [12,50,30], k = 4
Output: "There are less than 4 unique values"
Explanation: There are 3 unique values, so we return the error message
------------------------------------

"""


def kth_place(li: list, k: int):
    """
    HINTS:
    - sorting values of an iterable might be useful
    - you can access the last kth element of a list L by using L[-k]
    """
    data = list(set(li))
    data.sort(reverse=True)
    val = 0
    if len(data) >= k:
        for i in range(k): val = data[i]
    else: val = f"There are less than {k} unique values"
    return val


# print(kth_place([3,10,12,4,5,10], 3))
# print(kth_place([12,50,30], 4))