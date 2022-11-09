"""
In this file, you will need to
- create table "least_watched_categories" in destination database
- insert least watched categories to  table "least_watched_categories" in destination database
"""
from sqlalchemy import (
    Table,
    Column,
    Text,
    Integer,
)
from dags import (
    metadata_obj_destination,
    get_engine_destination,
    copy_data,
)


# IMPLEMENT THIS
def create_table_least_watched_categories():
    """Create table "least_watched_category" in destination database with the following constraints:
    - "category_id": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    - "count": INT
    """
    Table(
        "least_watched_category",
        metadata_obj_destination,
        Column("category_id", Integer, primary_key=True),
        Column("Category_name", Text, nullable=False, unique=True),
        Column("count", Integer),
    )
    metadata_obj_destination.create_all(get_engine_destination())


def insert_least_watched_categories():
    """insert category of videos that have the least number of views to table "least_watched_categories" in destination database.

    If there are multiple videos in a category C, then we count the total number of views
    for all such videos to represent C.

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    create table "least_watched_categories" first if there there is no table "least_watched_categories"

    """
    # """Return the category of videos that have the least number of views.

    # If there are multiple videos in a category C, then we count the total number of views
    # for all such videos to represent C.

    # Output a list of N categories ordered from the least watched.

    # If there are several users with the same watching duration, order alphabetically (e.g.
    # Alan is higher than Brown).

    # N: a positive integer

    # Example:
    #     N = 1
    #     return ["Film & Animation"]
    # """
    # query = run_query(
    #     f'''SELECT result."Category name", COUNT (result."Category name") AS total
    #     FROM (
    #         SELECT c."Category name", v.title, v.video_id
    #         FROM categories c
    #         INNER JOIN videos v ON c."ID" = v.category_id
    #     ) result
    #     INNER JOIN views ON views.video_id = result.video_id
    #     GROUP BY result."Category name"
    #     ORDER BY total
    #     LIMIT {N}'''
    # )
    # return [query[i]["Category name"] for i in range(N)]
    pass
