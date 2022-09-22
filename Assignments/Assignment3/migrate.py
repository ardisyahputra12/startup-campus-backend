"""
In this file, you will need to do the following:
- create a SQLite database
- move data from tables in PostgreSQL database to SQLite database

[DATA]
All data is available in the "public" schema. The following are the list of all 
tables you need to consider:
- Users
- Videos
- Views
- Categories


[CREDENTIAL]
- The credential to PostgreSQL database is available in Assignment3/creds.py
- If you have issues connecting with Python, try connecting with other tools such as Azure 
  Data Studio. If both attempts fail, please report immediately.

[TO DO & TIPS]
- Implement all functions with "# IMPLEMENT THIS" signs
- Feel free to implement any helper functions
"""


from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Float,
    Column,
    Table,
    MetaData,
    create_engine,
)

meta = MetaData()

# IMPLEMENT THIS
def create_sqlite_db():
    """Create a SQLite database with the name of assignment3.db

    Make sure it is stored in the correct path: Assignment/Assignments3/assignment3.db
    """
    return create_engine(
        "sqlite:///Assignment/Assignments3/assignment3.db",
        # echo = True,
        future = True
    )


# IMPLEMENT THIS
def create_table_users():
    """Create table "users" in SQLite with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "password": TEXT, can't be NULL
    - "followers": INT, default = 0
    - "registered_at": TEXT, can't be NULL
    """
    return Table(
        "users",
        meta,
        Column("user_id", String, primary_key=True),
        Column("name", String, nullable=False, unique=True),
        Column("password", String, nullable=False),
        Column("followers", Integer, default=0),
        Column("registered_at", nullable=False)
    )


# IMPLEMENT THIS
def copy_users():
    """Copy all rows in table "users" from PostgreSQL to SQLite."""
    pass


# IMPLEMENT THIS
def create_table_categories():
    """Create table "categories" in SQLite with the following constraints:
    - "ID": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    """
    return Table(
        "categories",
        meta,
        Column("ID", Integer, primary_key=True),
        Column("Category name", String, nullable=False, unique=True)
    )


# IMPLEMENT THIS
def copy_categories():
    """Copy all rows in table "categories" from PostgreSQL to SQLite."""
    pass


# IMPLEMENT THIS
def create_table_videos():
    """Create table "videos" in SQLite with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "length (min)": FLOAT/REAL, default = 0.0
    - "category_id": INT, linked with categories.id
    - "created_at": TEXT, can't be NULL
    """
    return Table(
        "videos",
        meta,
        Column("video_id", String, primary_key=True),
        Column("title", String, nullable=False),
        Column("length (min)", Float, default=0.0),
        Column("category_id", Integer, ForeignKey('categories.ID')),
        Column("created_at", String, nullable=False)
    )


# IMPLEMENT THIS
def copy_videos():
    """Copy all rows in table "videos" from PostgreSQL to SQLite."""
    pass


# IMPLEMENT THIS
def create_table_views():
    """Create table "views" in SQLite with the following constraints:
    - "view_id": TEXT, can't be NULL, must be unique
    - "user_id": TEXT, linked with users.user_id
    - "video_id": TEXT, linked with videos.video_id
    - "started_at": TEXT, can't be NULL
    - "finished_at": TEXT
    """
    return Table(
        "views",
        meta,
        Column("view_id", String, primary_key=True),
        Column("user_id", String, ForeignKey("users.user_id")),
        Column("video_id", String, ForeignKey("videos.video_id")),
        Column("started_at", String, nullable=False),
        Column("finished_at", String)
    )


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to SQLite."""
    pass
