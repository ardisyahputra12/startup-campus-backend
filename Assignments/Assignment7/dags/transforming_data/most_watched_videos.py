"""
In this file, you will need to
- create table "most_watched_videos" in destination database
-  insert most watched videos to table "most_watched_videos" in destination database
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


most_watched_videos = Table(
    "most_watched_videos",
    metadata_obj_destination,
    Column("video_id", Text, nullable=False, unique=True),
    Column("title", Text, nullable=False),
    Column("count", Integer),
)


# IMPLEMENT THIS
def create_table_most_watched_videos():
    """Create table "most_watched_videos" in destination database with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "count": INT
    """
    create_table(most_watched_videos, "most_watched_videos")


# IMPLEMENT THIS
def insert_most_watched_videos():
    """Insert the most watched videos to table "most_watched_videos" ordered from the most frequently watched videos.

    If there are multiple videos with same view count, rank the most recent video (based on
    Videos.created_at) higher in the list. For instance, if both videos V1 and V2 have 100 views
    and V1 is created earlier, than V2 should rank higher than V1 in the list.

    create table "most_watched_videos" if there is no table "most_watched_videos"

    """
    query = run_query_source("""
        SELECT v2.video_id, v2.title, COUNT(v.view_id) as "count"
        FROM "views" v
        JOIN videos v2 ON v2.video_id = v.video_id
        GROUP BY v2.video_id, v2.title, v2.created_at
        ORDER BY "count" DESC, v2.created_at DESC
    """)
    copy_data(create_table_most_watched_videos(), most_watched_videos, data=query)