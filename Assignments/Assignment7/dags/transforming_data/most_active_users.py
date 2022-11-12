"""
In this file, you will need to
- create table "most_active_users" in destination database
- insert most active users to table "most_active_users" in destination database
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
def create_table_most_active_users():
    """Create table "most_active_users" in destination table with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "duration": INT
    """
    Table(
        "most_active_users",
        metadata_obj_destination,
        Column("user_id", Text, primary_key=True),
        Column("name", Text, nullable=False, unique=True),
        Column("duration", Integer),
    )
    metadata_obj_destination.create_all(get_engine_destination())


# IMPLEMENT THIS (12 pts)
def insert_most_active_users():
    """Insert most active users to table "most_active_users" in destination database

    Total duration for a user is calculated as follows;
    - When a user U watches video V, it will be registered as a view (1 row on table Views)
    - The watching duration is NOT the length of V, but the difference between "finished_at"
        and "started_at" for each view
    - Accumulate the duration for all such views for user N
    - round the duration to the nearest integer and convert into MINUTES

    If there are several users with the same watching duration, order alphabetically (e.g.
    Alan is higher than Brown).

    Rounding happens after the sorting (e.g. Brown with 143.2 is still considered higher in
    the list than Alan with 143.1 even though both view time will be displayed as 143)

    create table "most_active_users" if there is no table "most_active_users"
    """
    query = run_query_source(
        f'''SELECT result.name, result.user_id, round(sum(duration)) AS total_duration
        FROM (
            SELECT name, user_id, EXTRACT(epoch FROM views.finished_at - views.started_at) / 60 AS duration
            FROM users
            INNER JOIN views ON users.user_id = views.user_id
        ) result
        GROUP BY result.name
        ORDER BY sum(duration) DESC, name
        '''
    )
    run_query_destination("DELETE FROM most_active_users", commit=True)
    for i in range(len(query)):
        q = f'''
            INSERT INTO most_active_users VALUES {
                query[i]["user_id"],
                query[i]["name"],
                query[i]["total_duration"]
        }'''
        run_query_destination(q, True)