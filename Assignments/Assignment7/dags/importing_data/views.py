"""
In this file, you will need to do the following:
- create table views in database "destination"
- move data from tables views in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

"""


def create_table_views():
    """Create table "views" in destination database with the following constraints:
    - "view_id": TEXT, can't be NULL, must be unique
    - "user_id": TEXT, linked with users.user_id
    - "video_id": TEXT, linked with videos.video_id
    - "started_at": TEXT, can't be NULL
    - "finished_at": TEXT
    """
    pass


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to destination database.

    create table views first if ther is no table views
    """
    pass
