"""
In this file, you will need to do the following:
- create table videos in database "destination"
- move data from tables videos in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

"""
from sqlalchemy import (
    Table,
    Column,
    Text,
    Float,
    Integer,
    ForeignKey,
)
from utils import (
    metadata_obj_destination,
    get_engine_destination,
    run_query_destination,
    run_query_source,
)


# IMPLEMENT THIS
def create_table_videos():
    """Create table "videos" in destination database with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "length (min)": FLOAT/REAL, default = 0.0
    - "category_id": INT
    - "created_at": TEXT, can't be NULL
    """
    Table(
        "videos",
        metadata_obj_destination,
        Column("video_id", Text, primary_key=True),
        Column("title", Text, nullable=False),
        Column("length (min)", Float, default = 0.0),
        Column("category_id", ForeignKey('categories.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=True),
        Column("created_at", Text, nullable=False),
    )
    metadata_obj_destination.create_all(get_engine_destination())


# IMPLEMENT THIS
def copy_videos():
    """Copy all rows in table "videos" from PostgreSQL to destination database.

    create table videos first if there is no table videos
    """
    data = run_query_source(f"SELECT * FROM videos")
    run_query_destination("DELETE FROM videos", commit=True)
    for el in data:
        if el["category_id"]==None: el["category_id"]=1
        # if "'" in el["title"]:
            # l=["'"]
            # el["title"]="".join(i for i in el["title"] if i not in l) 
            # e = el["title"].replace("'", "")
            # el["title"] = str(e)
            # if (e.startswith("'")==False) and (e.endswith("'")==False):
            #     el["title"] = "'" + e + "'"
            # else:
            #     el["title"] = e
        query = f'''INSERT INTO videos VALUES (
            '{el["video_id"]}',
            '{el["title"]}',
            '{el["length (min)"]}',
            '{el["category_id"]}',
            '{format(el["created_at"])}'
        )'''
        run_query_destination(query, commit=True)
