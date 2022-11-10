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
    insert,
)
from utils import (
    metadata_obj_destination,
    get_engine_destination,
    run_query_destination,
    run_query_source,
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
    query = run_query_source(
        f'''SELECT video_id, title, COUNT (views.view_id) AS total_view, created_at
        FROM videos
        JOIN views on views.video_id = videos.video_id
        GROUP BY title, created_at
        ORDER BY total_view DESC, created_at DESC
        '''
    )
    for i in range(len(query)):
        run_query_destination(
            insert(
                metadata_obj_destination.tables["most_watched_videos"]
            ).values(
                video_id= query[i]["video_id"],
                title=query[i]["title"],
                count=query[i]["total_view"]
            ), True
        )