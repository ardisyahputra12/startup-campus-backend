"""
In this file, you will need to do the following:
- create table users in database "destination"
- move data from tables users in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

"""

# IMPLEMENT THIS
def create_table_users():
    """Create table "users" in destination database with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "password": TEXT, can't be NULL
    - "followers": INT, default = 0
    - "registered_at": TEXT, can't be NULL
    """
    pass


# IMPLEMENT THIS
def copy_users():
    """Copy all rows in table "users" from PostgreSQL to destination database.

    create table users first if there is no table users

    """
    pass
