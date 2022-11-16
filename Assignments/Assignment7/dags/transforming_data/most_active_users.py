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
)
from utils import (
    create_table,
    copy_data,
    run_query_source,
    metadata_obj_destination,
)


most_active_users = Table(
    "most_active_users",
    metadata_obj_destination,
    Column("user_id", Text, nullable=False, unique=True),
    Column("name", Text, nullable=False, unique=True),
    Column("duration", Integer),
)


# IMPLEMENT THIS
def create_table_most_active_users():
    """Create table "most_active_users" in destination table with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "duration": INT
    """
    create_table(most_active_users, "most_active_users")


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
    query = run_query_source("""
        SELECT u.user_id, u."name", ROUND(SUM(EXTRACT(epoch FROM v.finished_at-v.started_at) / 60)) AS "duration"
        FROM users u
        JOIN "views" v ON v.user_id = u.user_id
        GROUP BY u.user_id, u."name"
        ORDER BY SUM(EXTRACT(epoch FROM v.finished_at-v.started_at) / 60) DESC, u."name"
    """)
    copy_data(create_table_most_active_users(), most_active_users, data=query)