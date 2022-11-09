from creds import (
    source_creds,
    destination_creds,
)
from sqlalchemy import (
    MetaData,
    create_engine,
    text,
    select,
    insert,
)


def get_engine(creds):
    engine = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        creds["user"],
        creds["pass"],
        creds["host"],
        creds["port"],
        creds["db"],
    )
    return create_engine(engine, future=True)

def get_engine_source():
    return get_engine(source_creds)

def get_engine_destination():
    return get_engine(destination_creds)

metadata_obj_source = MetaData(bind=get_engine_source())
metadata_obj_destination = MetaData(bind=get_engine_destination())

def get_query(engine, query, data, commit):
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query, data)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]

def run_query_source(query, data = None, commit: bool = False):
    return get_query(get_engine_source(), query, data, commit)

def run_query_destination(query, data = None, commit: bool = False):
    return get_query(get_engine_destination(), query, data, commit)

def copy_data(val):
    data = run_query_source(select(metadata_obj_source.tables[f"{val}"]))
    run_query_destination(insert(metadata_obj_destination.tables[f"{val}"]), data=data, commit=True)