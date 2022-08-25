# Basic unit testing
#
# Implement a logic in several way
# Check that student can create a test to cover cases.
# From our side, we will create
# - several false implementations (mesti ada yang salah 1)
# - 1 correct implementation (semua test case mesti bener)
#
# Misal:
#   find_smallest is a function to find the smallest positive integer in a list; if the list
#   doesn't contain any positive integers, return -1
#
# False attempt 1:
# def find_smallest(l: list):
#   return min(l) --> bakal salah kalau l mengandung angka non-positif
#
# False attempt 2:
# def find_smallest(l: list):
#   result = 1
#   for e in l:
#       if e < 0:        --> bakal salah kalau l mengandung 0, karena bakal return 0
#           continue
#       if result > e:
#         result = e
#
#


from unittest import TestCase

# this is the correct implementation
def find_smallest(l: list):
    # find the minimal positive integer
    res = min([e for e in l if e > 0])
    if res:
        return res

    # if no positive integers is found in the list
    return -1


class MyTest(TestCase):
    # you must satisfy the following:
    # - have at least 3 test-cases (3 points)
    # - all assertions must be valid when using the correct implementation (5 points)
    # - test case must have fail assertion on false implementations (7 points)
    cases = [
        # Test Case 1
        {"args": [3, 1, 2], "expected": 1}
        # continue below
    ]

    def test_find_smallest(self):
        for case in self.cases:
            self.assertEqual(find_smallest(case["args"]), case["expected"])


# run this file by:
#   cd to Assignment2 folder
#   python3.9 -m unittest -v p4.py
