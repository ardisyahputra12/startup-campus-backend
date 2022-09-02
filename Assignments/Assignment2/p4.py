"""
Crafting your test cases.

You are given the task to test a function "find_smallest", which should behave as follows:
  - return the smallest POSITIVE integer in a list
  - if the list doesn't contain any POSITIVE integers, return -1

Example for correct implementation of "find_smallest"
----------------------------------------------------------------------------------------------
Input: l = [3, 1, 2]
Output: 1
Explanation: The smallest integer in l is 1, and it's also positive so return 1
----------------------------------------------------------------------------------------------

As tester, you do not need to care about how the function is implemented. The main problem is
that test cases are not complete yet. You need to write at least 5 valid test cases, and your
test cases must cover 3 false implementations that are already prepared.

Grading scheme:
- # of TEST CASES: >= 5 test-cases (1 point per test case, up to 5 pts), must be unique
      (you can't simply copy paste a case, it will be detected by the grader)
- POSITIVE TESTING: all (unique) test cases must pass the assertion for correct
      implementation of find_smallest (4 pts * proportion of valid cases)
      e.g. if you input 5 unique cases, and 3 pass the test, then your score is
      4 * (3/5) = 2.4 pts
- NEGATIVE TESTING: test cases must have fail assertion on each of 3 false implementations
      (+2 pts if your test cases cover 1 false implementation, up to 6 pts)
- If you fail to test the correct implementation, then you will NOT get any point for 
  correctly covering any of the false implementations, so PLEASE make sure that your test
  cases are valid first
"""

from unittest import TestCase


# DO NOT EDIT THIS METHOD
# correct implementation
def find_smallest(l: list):
    positive_numbers = [e for e in l if e > 0]
    if not positive_numbers:
        return -1
    return min(positive_numbers)


class FindSmallestTest(TestCase):
    cases = [
        # Test Case 1, feel free to uncomment the following line
        {"l": [3, 1, 2], "expected": 1},
        # More test cases below
        {"l": [4, 0, 1], "expected": 1},
        {"l": [0, 0, 0], "expected": -1},
        {"l": [-1, 0.99, 1], "expected": 0.99},
        {"l": [], "expected": -1},
    ]

    # DO NOT EDIT THIS METHOD
    def test_valid(self):
        for case in self.cases:
            self.assertEqual(find_smallest(case["l"]), case["expected"])


# Test your cases by following these steps:
#   cd to Assignment2 folder
#   python3.9 -m unittest -v p4.py


# HINTS:
# - if you got stuck when creating test cases, check out the code for false implementations
#       in functions/find_smallest.py
# - think about edge cases carefully and re-read the problem description if necessary
