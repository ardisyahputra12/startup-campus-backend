"""
In this file, you will need to do the following:
- create table users in database "destination"
- move data from tables users in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

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
    metadata_obj_destination,
)


users = Table(
    "users",
    metadata_obj_destination,
    Column("user_id", Text, nullable=False, unique=True),
    Column("name", Text, nullable=False, unique=True),
    Column("password", Text, nullable=False),
    Column("followers", Integer, server_default="0"),
    Column("registered_at", Text, nullable=False),
)


# IMPLEMENT THIS
def create_table_users():
    """Create table "users" in destination database with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "password": TEXT, can't be NULL
    - "followers": INT, default = 0
    - "registered_at": TEXT, can't be NULL
    """
    create_table(users, "users")


# IMPLEMENT THIS
def copy_users():
    """Copy all rows in table "users" from PostgreSQL to destination database.

    create table users first if there is no table users

    """
    copy_data(create_table_users(), users, "users")