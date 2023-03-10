"""
Clean up sentences. [WEIGHT = 1]

Given a string, you need to clean up and remove unnecessary characters.
The only characters that are allowed are:
    - letters (a-z or A-Z)
    - numbers (0-9)
    - space character (" ")

Replace every other characters with a single space. And then, remove all spaces 
in the beginning and at the end of the string (leading/trailing spaces).

Finally, return the resulting string.

Examples
------------------------------------
Input: "I am learning Python3???"
Output: "I am learning Python3"
Explanation: Remove the question marks at the end
------------------------------------
Input: "Everything is good"
Output: "Everything is good"
Explanation: Nothing changes so return string as is
------------------------------------
Input: "    Independence day: August 17th, 1945 "
Output: "Independence day August 17th 1945"
Explanation: Replace the : and , and then remove all trailing/leading spaces
------------------------------------
"""


def clean_sentence(sentence: str) -> str:
    val = ""
    for i in range(len(sentence)):
        if sentence[i].isalnum(): val += sentence[i]
        else: val += " "
    return val.strip()


# print(clean_sentence("I am learning Python3???"))
# print(clean_sentence("Everything is good"))
# print(clean_sentence("    Independence day: August 17th, 1945 "))