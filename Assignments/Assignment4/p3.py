"""
Authentication.

In this problem, you will need to implement 2 endpoints, 1 for user registration and 1 for
login.

[REGISTRATION]

[[Endpoint]]
- Method: POST
- URL: /register
- Request body
    - username: string (required)
    - password: string (required)

[[Logic]]
0. If username or password is not given in the request body
    - return {"error": "Username or password is not given"}
    - status code; 400
1. registration will be valid if it satisfies all of these:
    - username hasn't been registered
    - password is NOT invalid (see point #3 below)
   on valid registration:
    - store user information in the SQLite database
    - return {"message": "Registration successful"}
    - status code: 201
2. when trying to register with a registered username
    - return {"error": "This username has been registered"}
    - status code: 409
3. when trying to register with an invalid password:
    - if password is less than 8 characters
        - return {"error": "Password must contain at least 8 characters"}
    - if password doesn't contain any letters
        - return {"error": "Password must contain a letter"}
    - if password doesn't contain any numbers
        - return {"error": "Password must contain a number"}
    - status code: 400

[LOGIN]

[[Endpoint]]
- Method: POST
- URL: /login
- Request body
    - username: string (required)
    - password: string (required)

[[Logic]]
0. If username or password is not given in the request body
    - return {"error": "Username or password is not given"}
    - status code; 400
1. login will be valid if it satisfies all these:
    - username has been registered
    - password is correct
   on valid login:
    - return {"message": "Login successful"}
    - status code: 200
2. when logging in with an unregistered user
    - return {"error": "Username is not registered"}
    - status code: 401
3. when logging in with a wrong password
    - return {"error": "Wrong password"}
    - status code: 401
"""
import os

from flask import Flask
from sqlalchemy import Column, MetaData, String, Table, create_engine, text


def get_engine():
    """Creating SQLite Engine to interact"""
    return create_engine("sqlite:///p3.db", future=True)


def create_app():
    app = Flask(__name__)

    # create table Users to store user information
    engine = get_engine()
    meta = MetaData()
    Table(
        "users",
        meta,
        Column("username", String, nullable=False, unique=True),
        Column("password", String, nullable=False, unique=True),
    )
    meta.create_all(engine)

    return app


app = create_app()


@app.route("/register", methods=["POST"])
def register():
    # IMPLEMENT THIS
    pass


@app.route("/login", methods=["POST"])
def login():
    # IMPLEMENT THIS
    pass


##############################################################################################
# Helper Methods
##############################################################################################


def run_query(query, commit: bool = False):
    """Runs a query against the given SQLite database.

    Args:
        commit: if True, commit any data-modification query (INSERT, UPDATE, DELETE)
    """
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]


# TEST IT YOURSELF
#   cd to Assignment4 folder
#   python3 p3.py
#
# please change the scenario as you wish
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    try:
        first_user_registration_response = c.post(
            "/register", json={"username": "Adam", "password": "Eve12345"}
        )
        assert first_user_registration_response.json == {
            "message": "Registration successful"
        }
        assert first_user_registration_response.status_code == 201

        invalid_reregister_response = c.post(
            "/register", json={"username": "Adam", "password": "Eve12345"}
        )
        assert invalid_reregister_response.json == {
            "error": "This username has been registered"
        }
        assert invalid_reregister_response.status_code == 409

        login_response = c.post(
            "/login", json={"username": "Adam", "password": "Eve12345"}
        )
        assert login_response.json == {"message": "Login successful"}
        assert login_response.status_code == 200

        print("Testing p3.py DONE!")
    finally:
        # remove DB if already exists
        db_name = "p3.db"
        if os.path.isfile(db_name):
            os.remove(db_name)
