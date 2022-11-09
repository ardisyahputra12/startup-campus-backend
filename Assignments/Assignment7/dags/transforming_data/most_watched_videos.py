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
from dags import (
    metadata_obj_destination,
    get_engine_destination,
    copy_data,
)


# IMPLEMENT THIS
def create_table_most_watched_videos():
    """Create table "most_watched_videos" in destination database with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "count": INT
    """
    Table(
        "most_watched_videos",
        metadata_obj_destination,
        Column("video_id", Text, primary_key=True),
        Column("title", Text, nullable=False),
        Column("count", Integer),
    )
    metadata_obj_destination.create_all(get_engine_destination())


# IMPLEMENT THIS
def insert_most_watched_videos():
    """Insert the most watched videos to table "most_watched_videos" ordered from the most frequently watched videos.

    If there are multiple videos with same view count, rank the most recent video (based on
    Videos.created_at) higher in the list. For instance, if both videos V1 and V2 have 100 views
    and V1 is created earlier, than V2 should rank higher than V1 in the list.

    create table "most_watched_videos" if there is no table "most_watched_videos"

    """
    # """Return the list of video titles, ordered from the most frequently watched videos.

    # If there are multiple videos with same view count, rank the most recent video (based on
    # Videos.created_at) higher in the list. For instance, if both videos V1 and V2 have 100 views
    # and V1 is created earlier, than V2 should rank higher than V1 in the list.

    # N: a positive integer

    # Example:
    #     N = 1,
    #     return ['headdress haploidy platitude sultry tapa anthropocentric knelt Catherine umbra devastate']
    # """
    # query = run_query(
    #     f'''SELECT title, COUNT (views.view_id) AS total_view, created_at
    #     FROM videos
    #     JOIN views on views.video_id = videos.video_id
    #     GROUP BY title, created_at
    #     ORDER BY total_view DESC, created_at DESC
    #     LIMIT {N}'''
    # )
    # return [query[i]["title"] for i in range(N)]
    pass
