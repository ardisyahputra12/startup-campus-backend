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
from utils import (
    create_table,
    copy_data,
    run_query_source,
    metadata_obj_destination,
)


least_watched_categories = Table(
    "least_watched_categories",
    metadata_obj_destination,
    Column("category_id", Integer, nullable=False, unique=True),
    Column("Category name", Text, nullable=False, unique=True),
    Column("count", Integer),
)


# IMPLEMENT THIS
def create_table_least_watched_categories():
    """Create table "least_watched_categories" in destination database with the following constraints:
    - "category_id": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    - "count": INT
    """
    create_table(least_watched_categories, "least_watched_categories")


# IMPLEMENT THIS
def insert_least_watched_categories():
    """insert category of videos that have the least number of views to table "least_watched_categories" in destination database.

    If there are multiple videos in a category C, then we count the total number of views
    for all such videos to represent C.

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    create table "least_watched_categories" first if there there is no table "least_watched_categories"

    """
    query = run_query_source("""
        SELECT v2.category_id, c."Category name", COUNT(v.video_id) as "count"
        FROM "views" v
        JOIN videos v2 ON v2.video_id = v.video_id
        JOIN categories c ON c."ID" = v2.category_id
        GROUP BY v2.category_id, c."Category name"
        ORDER BY "count"
    """)
    copy_data(create_table_least_watched_categories(), least_watched_categories, data=query)