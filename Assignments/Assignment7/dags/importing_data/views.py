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
    - "user_id": TEXT
    - "video_id": TEXT
    - "started_at": Datetime, can't be NULL
    - "finished_at": Datetime

    if table already exist, delete all data from table
    """
    pass


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to destination database.

    create table views first if there is no table views
    """
    pass
