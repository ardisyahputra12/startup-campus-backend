"""
In this file, you will need to
- create table "most_watched_videos" in destination database
-  insert most watched videos to table "most_watched_videos" in destination database
"""


# IMPLEMENT THIS
def create_table_most_watched_videos():
    """Create table "most_watched_videos" in destination database with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "count": INT
    """
    pass


# IMPLEMENT THIS
def insert_most_watched_videos():
    """Insert the most watched videos to table "most_watched_videos" ordered from the most frequently watched videos.

    If there are multiple videos with same view count, rank the most recent video (based on
    Videos.created_at) higher in the list. For instance, if both videos V1 and V2 have 100 views
    and V1 is created earlier, than V2 should rank higher than V1 in the list.

    create table "most_watched_videos" if there is no table "most_watched_videos"

    """
    pass
