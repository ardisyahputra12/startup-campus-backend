"""
In this file, you will need to do the following:
- create table views in database "destination"
- move data from tables views in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

"""
from sqlalchemy import (
    Table,
    Column,
    Text,
    DateTime,
    ForeignKey,
)
from utils import (
    metadata_obj_destination,
    get_engine_destination,
    run_query_destination,
    run_query_source,
)


def create_table_views():
    """Create table "views" in destination database with the following constraints:
    - "view_id": TEXT, can't be NULL, must be unique
    - "user_id": TEXT
    - "video_id": TEXT
    - "started_at": Datetime, can't be NULL
    - "finished_at": Datetime

    if table already exist, delete all data from table
    """
    # Table(
    #     "views",
    #     metadata_obj_destination,
    #     Column("view_id", Text, primary_key=True),
    #     Column("user_id", Text, ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    #     Column("video_id", Text, ForeignKey('videos.video_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    #     Column("started_at", DateTime, nullable=False),
    #     Column("finished_at", DateTime),
    # )
    # metadata_obj_destination.create_all(get_engine_destination())
    run_query_destination('''CREATE TABLE IF NOT EXISTS views (
        view_id TEXT NOT NULL,
        user_id TEXT,
        video_id TEXT,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        PRIMARY KEY (view_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (video_id) REFERENCES videos (video_id)
    )''', commit=True)


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to destination database.

    create table views first if there is no table views
    """
    data = run_query_source(f"SELECT * FROM views")
    create_table_views()
    run_query_destination("DELETE FROM views", commit=True)
    for el in data:
        query = f'''INSERT INTO views VALUES {
            el["view_id"],
            el["user_id"],
            el["video_id"],
            format(el["started_at"]),
            format(el["finished_at"])
        }'''
        run_query_destination(query, commit=True)
