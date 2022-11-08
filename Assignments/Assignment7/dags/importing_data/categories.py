"""
In this file, you will need to do the following:
- create table categories in database "destination"
- move data from tables categories in PostgreSQL "sources" database to PostgreSQL "destination" database 

Notes:
see creds.py for both db credential

"""

# IMPLEMENT THIS
def create_table_categories():
    """Create table "categories" in destination database with the following constraints:
    - "ID": INTEGER, can't be NULL, must be unique
    - "Category name": TEXT, can't be NULL, must be unique
    """
    pass


# IMPLEMENT THIS
def copy_categories():
    """Copy all rows in table "categories" from PostgreSQL to destination table.

    create table categories first if there is no table categories
    """
    pass
