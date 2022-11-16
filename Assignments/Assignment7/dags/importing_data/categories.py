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
    create_table,
    copy_data,
    metadata_obj_destination,
)


categories = Table(
    "categories",
    metadata_obj_destination,
    Column("ID", Integer, nullable=False, unique=True),
    Column("Category name", Text, nullable=False, unique=True),
)


# IMPLEMENT THIS
def create_table_categories():
    """Create table "categories" in destination database with the following constraints:
    - "ID": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    """    
    create_table(categories, "categories")


# IMPLEMENT THIS
def copy_categories():
    """Copy all rows in table "categories" from PostgreSQL to destination table.

    create table categories first if there is no table categories
    """    
    copy_data(create_table_categories(), categories, "categories")