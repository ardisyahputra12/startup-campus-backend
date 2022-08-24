"""
The smartest students. [WEIGHT = 2]

There are n (0 < n <= 100) students in the classroom, find out the student with 
the highest grade and return the name. Every student has unique names, always starts with
capital letter and will only contain letters or spaces.

If there are multiple such students, return a list of strings indicating their names, ordered
alphabetically.

If everyone has the same grade, return the message "All are winners" (even if there 
is only 1 student in the class)

The data is given in the form of dictionary student_grades, where
- key: student's name (or identifier of the student)
- value: student's grade (integer between 0 and 100, inclusive)

Examples
------------------------------------
Input: {"Alan": 80, "Bishop": 90, "Claire": 80}
Output: "Bishop"
Explanation: Bishop's grade (90) is higher than Alan/Claire (80)
------------------------------------
Input: {"Dwight": 80, "Bishop": 70, "Claire": 80}
Output: ["Claire", "Dwight"]
Explanation: Dwight and Claire are tied for the highest score in the class, and the highest_scorers
    is ordered alphabetically so Claire appears first in the list
------------------------------------
Input: {"Alan": 85, "Bishop": 85}
Output: "All are winners"
------------------------------------

"""


def smartest_students(student_grades: dict):
    """
    HINT:
    - you can compare 2 strings with comparison operator (<, > , etc.)
    - iterable that contains comparable objects, can be sorted
    """
    grades = [student_grades[i] for i in student_grades]
    val = [i for i in student_grades if student_grades[i] == max(grades)]
    val.sort()
    if len(val) == len(grades): val = "All are winners"
    elif len(val) > 1: return val
    else: return val[0]
    return val


# print(smartest_students({"Alan": 80, "Bishop": 90, "Claire": 80}))
# print(smartest_students({"Dwight": 80, "Bishop": 70, "Claire": 80}))
# print(smartest_students({"Alan": 85, "Bishop": 85}))