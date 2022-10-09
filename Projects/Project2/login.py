"""
Login.

After users registers, they can login to the marketplace to access all its functions.

[Endpoint]

You need to implement the following endpoint:
- URL: /login
- Method: POST
- Request body
    - username: string (required)
    - password: string (required)

Requirements (from the earliest to check):
- If username doesn't exist OR password is incorrect:
    - return {"error": "Username or password is incorrect"}
    - status code: 401
- If everything is valid:
    - return {"message": "Welcome to the marketplace", "token": <token>}
    - status code: 200
    - NOTE: 
        - token must be a UNIQUE string to identify a specific user
        - the next time the same user logins, a new, unique token will be generated
        - TIPS: you can consider using standard Python library uuid to generate a random
            string for each user (https://docs.python.org/3.9/library/uuid.html)
"""
import uuid
from flask import Blueprint, request
from utils import run_query, error_message, success_message

login_bp = Blueprint("login", __name__, url_prefix="/login")
token = uuid.uuid4()

@login_bp.route("", methods=["POST"])
def login():
    # IMPLEMENT THIS
    data = request.get_json()
    # Request body:
    #     - username: string (required)
    #     - password: string (required)

    if ("username" not in data) or ([{"password": data["password"]}] != run_query(f"SELECT password FROM users WHERE username = '{data['username']}'")):
        return error_message("Username or password is incorrect", 401)
    else:
        if [{"username": data["username"]}] == run_query(f"SELECT username FROM users WHERE password = '{data['password']}'"):
            run_query(f"UPDATE users SET token = '{token}'", commit=True)
        return success_message("Welcome to the marketplace", 200, token)
