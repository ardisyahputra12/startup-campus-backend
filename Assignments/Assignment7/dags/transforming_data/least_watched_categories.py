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
    insert,
)
from utils import (
    metadata_obj_destination,
    get_engine_destination,
    run_query_destination,
    run_query_source,
)


# IMPLEMENT THIS
def create_table_least_watched_categories():
    """Create table "least_watched_categories" in destination database with the following constraints:
    - "category_id": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    - "count": INT
    """
    Table(
        "least_watched_category",
        metadata_obj_destination,
        Column("category_id", Integer, primary_key=True),
        Column("category_name", Text, nullable=False, unique=True),
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
    query = run_query_source(
        f'''SELECT result."Category name", result.ID, COUNT (result."Category name") AS total
        FROM (
            SELECT c."Category name", c.ID, v.title, v.video_id
            FROM categories c
            INNER JOIN videos v ON c."ID" = v.category_id
        ) result
        INNER JOIN views ON views.video_id = result.video_id
        GROUP BY result."Category name"
        ORDER BY total
        '''
    )
    for i in range(len(query)):
        run_query_destination(
            insert(
                metadata_obj_destination.tables["least_watched_category"]
            ).values(
                category_id= query[i]["ID"],
                category_name=query[i]["Category name"],
                count=query[i]["total"]
            ), True
        )