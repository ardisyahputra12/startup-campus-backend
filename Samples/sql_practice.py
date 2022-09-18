# MIGRATION: moving data from 1 DB to the other
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    select,
    text,
)

from creds import pg_creds

##############################################################################################
# HELPER METHODS
##############################################################################################


def test_connect(engine):
    with engine.connect() as conn:
        print("Connected!")


# return hasil query
def execute_query(engine, query):
    with engine.connect() as conn:
        rows = conn.execute(text(query))
        for row in rows:
            # print(row) # row dalam bentuk tuple
            print(dict(row))  # row dalam bentuk column: value


if __name__ == "__main__":
    # print(pg_creds)
    user = pg_creds["user"]
    password = pg_creds["pass"]
    host = pg_creds["host"]
    port = pg_creds["port"]
    database = pg_creds["db"]

    engine = create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            user, password, host, port, database
        ),
        # echo=True,
        future=True,
    )

    # connect to a remote database (PostgreSQL)
    test_connect(engine)

    # check that we can select relevant data

    # cari berapa banyak rows di table users
    # execute_query(engine, "SELECT COUNT(*) FROM users")
    # execute_query(engine, "SELECT * FROM users LIMIT 5")
    # execute_query(engine, "CREATE TABLE things (name text)")
    # execute_query(engine, "DROP TABLE users")

    # create a local database (via SQLite)
    local_engine = create_engine(
        "sqlite:///example.db",
        # echo=True,
        future=True,
    )

    test_connect(local_engine)

    # add sample data
    import datetime

    sample_data = [
        {
            "user_id": "df1bac29-0b98-4350-b2bf-d7436edef93b",
            "name": "Landen West",
            "password": "15hy37uok9",
            "followers": 0,
            "registered_at": datetime.datetime(2017, 5, 26, 14, 30, 51, 537413),
        },
        {
            "user_id": "9052e357-2489-4561-8c18-aa7392717d93",
            "name": "Braydon Cherry",
            "password": "ap8uul3trj",
            "followers": 15,
            "registered_at": datetime.datetime(2013, 11, 21, 14, 30, 37, 755752),
        },
        {
            "user_id": "c3864fbd-4ca4-4630-8567-55c9b0ec3322",
            "name": "Carlee Sawyer",
            "password": "x1mqsnj5ha",
            "followers": 50,
            "registered_at": datetime.datetime(2008, 12, 11, 10, 22, 45, 109978),
        },
    ]

    # create tables
    # move table users from PostgreSQL
    with local_engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS users"))
        print("Table users is dropped")

        # if table already exists, drop the table
        # first, we create table called users in SQLite
        # query = (
        #     "CREATE TABLE IF NOT EXISTS users"
        #     + "(user_id TEXT, name TEXT, password TEXT, followers INTEGER, registered_at TEXT)"
        # )
        # print("sebelum create table")
        # conn.execute(text(query))
        # print("sesudah create table")

        # ALTERNATIVE: creating table with SQLAlchemy Metadata
        metadata_obj = MetaData()

        # defining tables
        user_table = Table(
            "users",
            metadata_obj,
            Column("user_id", String, primary_key=True),
            Column("name", String, nullable=False),
            Column("password", String),
            Column("followers", Integer),
        )
        video_table = Table("videos", metadata_obj, Column("video_id", String))
        # kita create semua table yang disimpan di metadata
        metadata_obj.create_all(local_engine)
        print("ALl table are created")

        # apakah table ini sudah dibuat di Database?

        # insert data
        # conn.execute(
        #     text(
        #         "INSERT INTO users (user_id, name, password, followers, registered_at)"
        #         + " values (:user_id, :name, :password, :followers, :registered_at)"
        #     ),
        #     sample_data,
        # )
        # print("New user is added")

        # ALTERNATIVE: insert with SQLAlchemy ORM
        result = conn.execute(insert(user_table), sample_data)
        conn.commit()

        # check that table users is already created
        # rows = conn.execute(text("SELECT * FROM users"))
        rows = conn.execute(select(user_table).where(user_table.c.followers > 30))
        print("USERS: ", rows.all())

        rows = conn.execute(text("SELECT * FROM videos"))
        print("VIDEOS: ", rows.all())

        print("all data are selected")

    # add relevant constraints

    # insert data from remote DB to local DB
