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
    copy_data,
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
    Table(
        "views",
        metadata_obj_destination,
        Column("view_id", Text, primary_key=True),
        Column("user_id", Text, ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE')),
        Column("video_id", Text, ForeignKey('videos.video_id', ondelete='CASCADE', onupdate='CASCADE')),
        Column("started_at", DateTime, nullable=False),
        Column("finished_at", DateTime),
    )
    metadata_obj_destination.create_all(get_engine_destination())


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to destination database.

    create table views first if there is no table views
    """
    copy_data("views")
