"""
In this file, you will need to
- create table "least_watched_categories" in destination database
- insert least watched categories to  table "least_watched_categories" in destination database
"""


# IMPLEMENT THIS
def create_table_least_watched_categories():
    """Create table "least_watched_categories" in destination database with the following constraints:
    - "category_id": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    - "count": INT
    """
    pass


def insert_least_watched_categories():
    """insert category of videos that have the least number of views to table "least_watched_categories" in destination database.

    If there are multiple videos in a category C, then we count the total number of views
    for all such videos to represent C.

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    create table "least_watched_categories" first if there there is no table "least_watched_categories"

    """
    pass
