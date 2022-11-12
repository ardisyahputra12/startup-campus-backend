"""
In this file, you will need to do the following:
- create table categories in database "destination"
- move data from tables categories in PostgreSQL "sources" database to PostgreSQL "destination" database 

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
    metadata_obj_destination,
    get_engine_destination,
    run_query_destination,
    run_query_source,
)


# IMPLEMENT THIS
def create_table_categories():
    """Create table "categories" in destination database with the following constraints:
    - "ID": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    """
    Table(
        "categories",
        metadata_obj_destination,
        Column("ID", Integer, primary_key=True),
        Column("Category name", Text, nullable=False, unique=True),
    )
    metadata_obj_destination.create_all(get_engine_destination())


# IMPLEMENT THIS
def copy_categories():
    """Copy all rows in table "categories" from PostgreSQL to destination table.

    create table categories first if there is no table categories
    """
    data = run_query_source(f"SELECT * FROM categories")
    run_query_destination("DELETE FROM categories", commit=True)
    for el in data:
        query = f'''INSERT INTO categories VALUES {
            el["ID"],
            el["Category name"]
        }'''
        run_query_destination(query, commit=True)