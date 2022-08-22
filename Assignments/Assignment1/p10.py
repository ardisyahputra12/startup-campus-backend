"""
Summarize subject scores. [WEIGHT = 3]

Given 2 inputs:
- scores: a list of dictionary represeting student details:
    - name: student name (names will be unique)
    - science: student's science score
    - math: student's math score
    - computer: student's computer score
    all scores are integers between 0 and 100, inclusive. 
- subject: the selected subject to summarize, must be one of "science", "math" or "computer"

For the selected subject, calculate the following summary:
- average: the average score for this subject across all students, 
    rounded up
- highest: the highest score with the list of student names (if more than 1 student got the
    highest score, then list all the names and order alphabetically)
- lowest: similar to highest, but for lowest score

Format the result as follows:
{
    "average": <average score>, 
    "highest": {"score": <maximum score>, "names": [...]}, 
    "lowest": {"score": <minimum score>, "names": [...]}, 
}

If no student data appears, then set all scores to be 0 and "names" should be empty list

Examples
------------------------------------------------------------------------
Input: scores = [
        {"name": "Santi", "science": 60, "math": 90, "computer": 100}, 
        {"name": "Joko", "science": 50, "math": 90, "computer": 30}, 
        {"name": "Budi", "science": 80, "math": 30, "computer": 30}, 
        {"name": "Beri", "science": 40, "math": 80, "computer": 60}
    ]
    subject = "science"
Output: 
    {
        "average": 58,
        "highest": {"score": 80, "names": ["Budi"]},
        "lowest": {"score": 40, "names": ["Beri"]}
    }
Explanation: 
- average score for science is (50+80+60+40)/4 = 57.5, but rounded to 58
------------------------------------------------------------------------
Input: scores = [
        {"name": "Santi", "science": 60, "math": 90, "computer": 100}, 
        {"name": "Joko", "science": 50, "math": 90, "computer": 30}, 
        {"name": "Budi", "science": 80, "math": 30, "computer": 30}, 
        {"name": "Beri", "science": 40, "math": 80, "computer": 60}
    ]
    subject = "math"
Output: 
    {
        "average": 73,
        "highest": {"score": 90, "names": ["Joko", "Santi"]},
        "lowest": {"score": 30, "names": ["Budi"]}
    }
Explanation: 
- average math score is (90+30+90+80)/4 = 72.5, but rounded to 73
- two people got the same highest score (90)
------------------------------------------------------------------------
"""


def summarize_subject_scores(scores: list, subject: str) -> dict:
    """HINTS: you may follow the pseudocode, or feel free to implement your own solution"""
    # create a function to get a dictionary, mapping student name to his/her grade on
    # selected subject, the function should return something like the following
    #   {"name1": grade1, "name2": grade2, ...}
    student_names_to_grades = map_name_to_grade(scores, subject)

    # calculate average
    average = None

    # calculate highest score
    highest_score = None
    # calculate all students getting the highest score
    highest_scorers = get_scorers(student_names_to_grades, highest_score)

    # calculate lowest score
    lowest_score = None
    # calculate all students getting the lowest score
    lowest_scorers = get_scorers(student_names_to_grades, lowest_score)

    # final formatting
    return {"average": None, "highest": {}, "lowest": {}}


##############################################################################################
# Feel free to NOT use the following helper method(s)
##############################################################################################


def map_name_to_grade(scores: list, subject: str) -> dict:
    """Returns a mapping between student name to his/her score for the given subject"""
    pass


def get_scorers(names_to_scores: dict, score: int) -> list:
    """Returns a list of names whose score equal the given score
    and order the result alphabetically."""
    pass
