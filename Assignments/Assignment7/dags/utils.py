from creds import (
    source_creds,
    destination_creds,
)
from sqlalchemy import (
    MetaData,
    create_engine,
    inspect,
    text,
    insert,
)


# Create Engine
# =================================================================================
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


# Variable Metadata
# =================================================================================
metadata_obj_source = MetaData(bind=get_engine_source())
metadata_obj_destination = MetaData(bind=get_engine_destination())


# Run Query
# =================================================================================
def get_query(engine, query, data, commit):
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            if data is None:
                conn.execute(query)
            else:
                conn.execute(query, data)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]

def run_query_source(query, data=None, commit:bool=False):
    return get_query(get_engine_source(), query, data, commit)

def run_query_destination(query, data=None, commit:bool=False):
    return get_query(get_engine_destination(), query, data, commit)


# Create Table
# =================================================================================
def create_table(table, table_name):
    if not inspect(get_engine_destination()).has_table(table_name):
        table
        metadata_obj_destination.create_all(get_engine_destination())
    else:
        run_query_destination(f"DELETE FROM {table_name}", commit=True)


# Copy Data
# =================================================================================
def copy_data(create_table, destination_table, source_table_name=None, data=None):
    if data is None:
        data = run_query_source(f"SELECT * FROM {source_table_name}")

    create_table
    run_query_destination(insert(destination_table), data=data, commit=True)