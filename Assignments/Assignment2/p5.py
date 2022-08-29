"""
Ace your assertions.

In this problem, you need to implement your own test function and make sure you create your 
own cases and assertions.

Test the function "the_lucky_winner" which have the following requirements

INPUT
- names: a list of strings representing people's names
- lottery_numbers: a list of integers between 1 and 1000 (inclusive), each number
    belongs to each person in "names", in the same respective order 
- N: a positive integer representing the initial "lucky number"

HOW IT WORKS:
1. the lucky number N will be first presented to the crowd
2. if there is a person whose lotter number is equal to the lucky number, then he/she is
    the winner
3. otherwise, we generate a new lucky number N' which is about half as small as 
   the previous one:
    - if N is even, then the new number N' = N/2
    - if N is odd, then the new number N' = (N-1)/2
4. repeat step 2 and 3, until we find a winner OR the lucky number reaches 0

PROBLEMS:
- It's possible that names are not unique (there can be 2 people with the same name)
- It's possible that the lottery numbers are not unique

RULES & OUTPUT (in this order):
- If two people have the same name, return "Found duplicate participants"
- If two people have the same lottery number, return "Found duplicate numbers"
- If a lucky winner exists, return the name of the lucky winner
- If a lucky winner can't be found, return "No winner this time"

Examples
----------------------------------------------------------------------------------------------
Input: 
    names = ["Abdul", "Modena", "Zeno"]
    lottery_number = [17, 35, 99]
    N = 69
Output: "Abdul"
Explanation: 
- Abdul's number is 17, Modena's is 35, Zeno's is 99
- Initially, the lucky number is 69 > no one has this lottery number
- Generate the new lucky number > (69-1)/2 = 34 > again no one has this lottery number 
  (Modena's number is very close at 35, but not exactly)
- Generate the next lucky number > 34/2 = 17 > Abdul has this number so he takes
----------------------------------------------------------------------------------------------

Your unit test will need to cover the following:
- 1 correct implementation
- 4 false implementations

Grading scheme:
- Please assert using the function "the_lucky_winner" that is already imported for you
- Write your assertions in test_valid (max: 15 pts) 
    - all the assertions must be passed for the correct implementation (+3 pts)
    - some of the assertions must fail for the false implmentations (+3 pts each)
    - if you fail to test the correct implementation, then you will NOT get any point for
      correctly covering any of the false implementations, so PLEASE make sure that your test
      cases are valid first
"""
# DO NOT EDIT
from unittest import TestCase

# DO NOT EDIT
from functions.the_lucky_winner import the_lucky_winner


class LuckyWinnerTest(TestCase):
    # please implement this
    def test_valid(self):
        pass


# Test your positive cases by following these steps:
#   cd to Assignment2 folder
#   python3.9 -m unittest -v p5.py

# HINTS:
# - if you got stuck when creating test cases, check out the code for false implementations
#       in functions/the_lucky_winner.py
# - think about edge cases carefully and re-read the problem description if necessary
