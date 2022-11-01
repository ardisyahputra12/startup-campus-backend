from sqlalchemy import create_engine
from creds import source_creds, destination_creds


def source_pg_engine():
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        source_creds["user"],
        source_creds["pass"],
        source_creds["host"],
        source_creds["port"],
        source_creds["db"],
    )
    return create_engine(engine_uri)


def destination_pg_engine():
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        destination_creds["user"],
        destination_creds["pass"],
        destination_creds["host"],
        destination_creds["port"],
        destination_creds["db"],
    )
    return create_engine(engine_uri)
