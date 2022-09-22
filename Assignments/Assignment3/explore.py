"""
In this file, you will need to
- connect to a PostgreSQL remote database
- create and execute SQL queries to find the desired data

[DATA]
All data is available in the "public" schema. The following are the list of all 
tables you need to consider:
- Users: unique users
- Videos: unique videos
- Views: watching activities, each activity = 1 user watch 1 video
- Categories: list of video categories (attached to video)

[CREDENTIAL]
- The credential to PostgreSQL database is available in Assignment3/creds.py
- If you have issues connecting with Python, try connecting with other tools such as Azure 
  Data Studio. If both attempts fail, please report immediately.

[TO DO & TIPS]
- Implement all functions with "# IMPLEMENT THIS" signs
- Feel free to implement any helper functions
- Check all column names of each tables with either:
    - simple query such as "SELECT * FROM <tablename> LIMIT 1"
    - Table object from SQLAlchemy as follows

        from sqlalchemy import MetaData, Table

        engine = create_engine(...)
        metadata = MetaData(bind=engine)
        table = Table(<table_name>, metadata, autoload=True)
        columns = [col.name for col in table.c] 
        print(columns)
"""
from typing import List


# IMPLEMENT THIS (3 pts)
def count_users() -> int:
    """Return # of unique users"""
    pass


# IMPLEMENT THIS (5 pts)
def count_videos(length: int) -> int:
    """Return # of unique videos whose length is (strictly) less than the given length.

    length: an integer

    Example:
        if length = 10, return 156
    """
    pass


# IMPLEMENT THIS (5 pts)
def oldest_videos(N: int) -> List[str]:
    """Return the list of N video titles ordered from the oldest ones (based on created_at).

    N: a positive integer

    Example:
        N = 1
        return ["Triangulum Ft woodside cohosh pendulous downstream opal buckthorn sundown"]
    """
    pass


# IMPLEMENT THIS (7 pts)
def most_watched_videos(N: int) -> List[str]:
    """Return the list of video titles, ordered from the most frequently watched videos.

    If there are multiple videos with same view count, rank the most recent video (based on
    Videos.created_at) higher in the list. For instance, if both videos V1 and V2 have 100 views
    and V1 is created earlier, than V2 should rank higher than V1 in the list.

    N: a positive integer

    Example:
        N = 1,
        return ['headdress haploidy platitude sultry tapa anthropocentric knelt Catherine umbra devastate']
    """
    pass


# IMPLEMENT THIS (12 pts)
def most_active_users(N: int) -> List[List]:
    """Return top N users with the longest watching activity.

    Total duration for a user is calculated as follows;
    - When a user U watches video V, it will be registered as a view (1 row on table Views)
    - The watching duration is NOT the length of V, but the difference between "finished_at"
        and "started_at" for each view
    - Accumulate the duration for all such views for user N
    - Convert the duration into MINUTES

    Output a list of [username, duration] and we round the duration to the nearest integer.

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    Rounding happens after the sorting (e.g. Brown with 143.2 is still considered higher in
    the list than Alan with 143.1 even though both view time will be displayed as 143)

    N: a positive integer

    Example:
        N = 3,
        return [
            ["Francis Frank", 911.0],
            ["Renee Fitzgerald", 825.0],
            ["Rylee Giles", 815.0]
        ]
    """
    pass


# IMPLEMENT THIS (10 pts)
def least_watched_categories(N: int) -> str:
    """Return the category of videos that have the least number of views.

    If there are multiple videos in a category C, then we count the total number of views
    for all such videos to represent C.

    Output a list of N categories ordered from the least watched.

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    N: a positive integer

    Example:
        N = 1
        return ["Film & Animation"]
    """
    pass


def run_query(query: str) -> List[dict]:
    from sqlalchemy import create_engine

    from creds import pg_creds

    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        pg_creds["user"],
        pg_creds["pass"],
        pg_creds["host"],
        pg_creds["port"],
        pg_creds["db"],
    )
    engine = create_engine(engine_uri)

    with engine.connect() as conn:
        print("Connected")
        return [dict(row) for row in conn.execute(query)]

# print(run_query("select * from videos"))