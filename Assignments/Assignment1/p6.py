"""
Factorial. [WEIGHT = 1]

Given an integer n (n <= 20), find the factorial of n (usually formulated as n!).

Factorial of n can be described as the multiplication of n with all positive integers
less than n. In other words, n! = n * (n-1) * ... * 1
 
If n is less than 0, return -1 and if n = 0, return 1.

Enamples
------------------------------------
Input: 5
Output: 120
Explanation: 5*4*3*2*1 = 120
------------------------------------
Input: 10
Output: 3628800
Explanation: 10*9*8*7*6*5*4*3*2*1 = 3628800
------------------------------------
"""


def factorial(n: int) -> int:
    val = 1
    if n < 0: val = -1
    elif n == 0: val = 1
    for i in range(n, 1, -1): val *= i
    return val


# print(factorial(5))
# print(factorial(10))