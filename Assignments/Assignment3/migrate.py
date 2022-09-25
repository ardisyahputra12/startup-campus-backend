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
    select,
    insert,
    text
)

from explore import run_query

metadata_obj = MetaData()


# IMPLEMENT THIS
def create_sqlite_db():
    """Create a SQLite database with the name of assignment3.db

    Make sure it is stored in the correct path: Assignment/Assignments3/assignment3.db
    """
    # Assignments/Assignment3
    engine = create_engine(
        "sqlite:///assignment3.db",
        # echo = True,
        future = True
    )
    engine.connect()
    return engine


# CREATE TABLE
def create_table(query):
    with create_sqlite_db().connect() as conn:
        conn.execute(text(query))


# IMPLEMENT THIS
def create_table_users():
    """Create table "users" in SQLite with the following constraints:
    - "user_id": TEXT, can't be NULL, must be unique
    - "name": TEXT, can't be NULL, must be unique
    - "password": TEXT, can't be NULL
    - "followers": INT, default = 0
    - "registered_at": TEXT, can't be NULL
    """
    # return Table(
    #     "users",
    #     metadata_obj,
    #     Column("user_id", String, primary_key=True),
    #     Column("name", String, nullable=False, unique=True),
    #     Column("password", String, nullable=False),
    #     Column("followers", Integer, default=0),
    #     Column("registered_at", String, nullable=False)
    # ).create(create_sqlite_db())
    query = '''CREATE TABLE users (
        user_id TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        followers INTEGER DEFAULT 0,
        registered_at TEXT NOT NULL,
        PRIMARY KEY (user_id)
    )'''
    create_table(query)
    return query


# IMPLEMENT THIS
def copy_users():
    """Copy all rows in table "users" from PostgreSQL to SQLite."""
    with create_sqlite_db().connect() as conn:
        for users in run_query("SELECT * FROM users"):
            query = f'''INSERT INTO users VALUES {
                users["user_id"],
                users["name"],
                users["password"],
                users["followers"],
                format(users["registered_at"])
            }'''
            conn.execute(text(query))
            conn.commit()


# IMPLEMENT THIS
def create_table_categories():
    """Create table "categories" in SQLite with the following constraints:
    - "ID": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    """
    # return Table(
    #     "categories",
    #     metadata_obj,
    #     Column("ID", Integer, nullable=False, unique=True),
    #     Column("Category name", String, nullable=False, unique=True)
    # ).create(create_sqlite_db())
    query = '''CREATE TABLE categories (
        ID INTEGER NOT NULL UNIQUE,
        'Category name' TEXT NOT NULL UNIQUE
    )'''
    create_table(query)
    return query


# IMPLEMENT THIS
def copy_categories():
    """Copy all rows in table "categories" from PostgreSQL to SQLite."""
    with create_sqlite_db().connect() as conn:
        for categories in run_query("SELECT * FROM categories"):
            query = f'''INSERT INTO categories VALUES {
                categories["ID"],
                categories["Category name"]
            }'''
            conn.execute(text(query))
            conn.commit()


# IMPLEMENT THIS
def create_table_videos():
    """Create table "videos" in SQLite with the following constraints:
    - "video_id": TEXT, can't be NULL, must be unique
    - "title": TEXT, can't be NULL
    - "length (min)": FLOAT/REAL, default = 0.0
    - "category_id": INT, linked with categories.id
    - "created_at": TEXT, can't be NULL
    """
    # return Table(
    #     "videos",
    #     metadata_obj,
    #     Column("video_id", String, primary_key=True),
    #     Column("title", String, nullable=False),
    #     Column("length (min)", Float, server_default="0.0"),
    #     Column("category_id", Integer, ForeignKey('categories.ID')),
    #     Column("created_at", String, nullable=False)
    # ).create(create_sqlite_db())
    query = '''CREATE TABLE videos (
        video_id TEXT NOT NULL,
        title TEXT NOT NULL,
        'length (min)' FLOAT DEFAULT 0.0,
        category_id INTEGER,
        created_at TEXT NOT NULL,
        PRIMARY KEY (video_id),
        FOREIGN KEY (category_id) REFERENCES categories (ID)
    )'''
    create_table(query)
    return query


# IMPLEMENT THIS
def copy_videos():
    """Copy all rows in table "videos" from PostgreSQL to SQLite."""
    with create_sqlite_db().connect() as conn:
        for videos in run_query("SELECT * FROM videos"):
            if videos["category_id"] == None: videos["category_id"] = "Null"
            query = f'''INSERT INTO videos VALUES {
                videos["video_id"],
                videos["title"],
                videos["length (min)"],
                videos["category_id"],
                format(videos["created_at"])
            }'''
            conn.execute(text(query))
            conn.commit()


# IMPLEMENT THIS
def create_table_views():
    """Create table "views" in SQLite with the following constraints:
    - "view_id": TEXT, can't be NULL, must be unique
    - "user_id": TEXT, linked with users.user_id
    - "video_id": TEXT, linked with videos.video_id
    - "started_at": TEXT, can't be NULL
    - "finished_at": TEXT
    """
    # return Table(
    #     "views",
    #     metadata_obj,
    #     Column("view_id", String, primary_key=True),
    #     Column("user_id", String, ForeignKey("users.user_id")),
    #     Column("video_id", String, ForeignKey("videos.video_id")),
    #     Column("started_at", String, nullable=False),
    #     Column("finished_at", String)
    # ).create(create_sqlite_db())
    query = '''CREATE TABLE views (
        view_id TEXT NOT NULL,
        user_id TEXT,
        video_id TEXT,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        PRIMARY KEY (view_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (video_id) REFERENCES videos (video_id)
    )'''
    create_table(query)
    return query


# IMPLEMENT THIS
def copy_views():
    """Copy all rows in table "views" from PostgreSQL to SQLite."""
    with create_sqlite_db().connect() as conn:
        for views in run_query("SELECT * FROM views"):
            query = f'''INSERT INTO views VALUES {
                views["view_id"],
                views["user_id"],
                views["video_id"],
                format(views["started_at"]),
                format(views["finished_at"])
            }'''
            conn.execute(text(query))
            conn.commit()
