"""
Pet identity.

You are given a Pet class, which has several attributes:
- name: name of the pet (string)
- type: type of pet (string)
- birth_year: (OPTIONAL) if given, the birth year of the pet; otherwise, set to 2020

You are required to implement these missing functionalities for class Pet:

[Class Attributes]
- name: the name of the pet
- type: the type of the pet

[Class Methods]
- age(year): return the age of the pet, which is the year difference between 
    input argument (year) and the birth year of this pet; if argument "year" is earlier
    than the birth year of this pet, return "Not applicable"
- same_type(year, other_pet): return whether this pet and other_pet has the same type

Examples
----------------------------------------------------------------------------------------------
Input: 
    - pet1 = Pet("Charlie", "cat", birth_year=2003)
    - pet2 = Pet("Dante", "dog", birth_year=2005)
    - pet3 = Pet("Simba", "cat")

Query: pet1.name
Output: "Charlie"  
Explanation: pet1.name refers to the name of the 1st pet, which is "Charlie"

Query: pet2.type
Output: "dog"
Explanation: pet2.type refers to the type of the 2nd pet, which is "dog"

Query: pet2.age(2010)
Output: 5
Explanation: year=2010, and the birth year of pet2 is 2005, so age is 2010 - 2005 = 5 (years)

Query: pet3.same_type(pet1)
Output: True
Explanation: Both pet3 and pet1 have the same type "cat", so return True

Query: pet3.age(2022)
Output: 2
Explanation: birth_year for pet3 is not specified, so it defaults to 2020 and input year is
    2022; therefore the age of pet3 is 2022 - 2020 = 2 (years)

Query: pet2.same_type(pet3)
Output: False
Explanation: pet2 is a dog, while pet3 is a cat; so return False
----------------------------------------------------------------------------------------------
"""


class Pet:
    def __init__(self, name: str, type: str, birth_year: int = None):
        pass

    def age(self, year: int):
        pass

    def same_type(self, other_pet):
        pass


# Test your code by uncommenting the following code and modify accordingly
# pets = [
#     Pet("Charlie", "cat", birth_year=2003),
#     Pet("Dante", "dog", birth_year=2005),
#     Pet("Simba", "cat"),
# ]
# print(pets[0].name)
# print(pets[1].age(2010))
#
# and then run the following comand
#       python3.9 p1.py
# from within folder Assignment 2
