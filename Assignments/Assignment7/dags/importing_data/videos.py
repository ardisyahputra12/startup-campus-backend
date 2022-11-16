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
)
from utils import (
    create_table,
    copy_data,
    metadata_obj_destination,
)


videos = Table(
    "videos",
    metadata_obj_destination,
    Column("video_id", Text, nullable=False, unique=True),
    Column("title", Text, nullable=False),
    Column("length (min)", Float, server_default = "0.0"),
    Column("category_id", Integer, nullable=True),
    Column("created_at", Text, nullable=False),
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
    create_table(videos, "videos")


# IMPLEMENT THIS
def copy_videos():
    """Copy all rows in table "videos" from PostgreSQL to destination database.

    create table videos first if there is no table videos
    """
    copy_data(create_table_videos(), videos, "videos")