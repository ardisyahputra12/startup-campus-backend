"""
Student administration.

You are given a list of student information. Each information contains the 
following attributes:
- first_name: first name of the student (string)
- last_name: last name of the student (string)
- grades: list of grades for this student (list of floats)

Your tasks are the following:
1. Override __str__ function so that when you print Student object, it will display
        "[<first_name> <last_name>] - score: <total_score>"
   where total score is the sum of all grades for this student, ROUNDED UP.
2. Override __eq__ and __lt__ so that we can compare 2 Student objects with normal 
   comparison operators. The comparison is based on the TOTAL SCORE for each student based
   on the grades:
   - if Student1 scores higher than Student 2, than Student1 > Student2 should return True
   - if both students score the same, then Student1 == Student2 should return True
3. Implement methods highest_grade and lowest_grade to get highest/lowest grade that each 
    student obtains.

NOTES:
- if grades is given as an empty list, then treat as if the student has a total score of 0,
    and his/her highest and lowest score is also 0

Examples
----------------------------------------------------------------------------------------------
Input: 
    - student1 = Student("Adam", "Smith", grades=[90, 80])
    - student2 = Student("Bryant", "Lenin", grades=[70, 65.3])
    - student3 = Student("Claire", "Voy", grades=[72.8, 97.2])

Query: print(student1)
Output: should display "[Adam Smith] - score: 170"
Explanation: print format follows the instruction, total score for Adam is 90+80 = 170

Query: student1 < student2
Output: False
Explanation: total score for student1 is 170, while student2 has 70+65.3 = 135.3, since
    the score for student1 is higher, then this comparison is False

Query: student3 <= student1
Output: True
Explanation: total score for student1 is 170, while student2 has 72.8+97.2 = 17-, since
    both students have the same score, then this comparison is True

Query: student1.highest_score
Output: 90
Explanation: student1 has 2 grades: 90, 80, so return the highest one: 90
"""
from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, first_name: str, last_name: str, grades: list):
        pass

    # override this to print
    # return string in the format of "[<first_name> <last_name>] - score: <total_score>"
    def __str__(self):
        pass

    # implement this to compare this Student and other student
    # returns True if and only if both students have the same
    def __eq__(self, other_student: object) -> bool:
        pass

    # implement this
    # returns True if and only if this student has lower score than other student
    def __lt__(self, other_student: object) -> bool:
        pass

    # implement this
    def highest_score(self) -> float:
        pass

    # implement this
    def lowest_score(self) -> float:
        pass

    # feel free to add other helper methods


# Test your code by uncommenting the following code and modify accordingly
# student1 = Student("Adam", "Smith", grades=[90, 80])
# student2 = Student("Bryant", "Lenin", grades=[70, 65.3])
# student3 = Student("Claire", "Voy", grades=[72.8, 97.2])
#
# print(student1)
# print(student1 < student2)  # should return False
# print(student1.highest_score())  # should return 90
#
# and then run the following comand
#       python3 p2.py
# from within folder Assignment 2
