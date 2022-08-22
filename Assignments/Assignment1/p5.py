"""
Find information by label. [WEIGHT = 1]

Given 3 inputs:
- labels: a list of unique strings representing labels
- info: a list of information corerespond to each label in the same order
     (len(info) = len(labels))
- query: a single string, representing individual label

Find the information that corresponds to label query, and return the string. Checking the
label must be case-sensitive (label "Name" is different with "name").

If label to query is not found in labels, return "Information not available"

Examples
------------------------------------
Input: labels = ["club_name", "score", "captain"], info = ["manchester united", "4-0", "maguire"] data_key = "score"
Output: "4-0"
Explanation: In this example. "score" is the 2nd label, so return the 2nd entry in info which is "4-0"
------------------------------------
Input: labels = ["name", "age", "birthday"], info = ["jhony", 21, "August 14, 1995"], query = "score"
Output: "Information not available"
Explanation: Label "score" doesn't exist in labels
------------------------------------
"""


def find_by_label(labels: list, info: list, query: str):
    pass
