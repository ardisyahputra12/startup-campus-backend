from flask import Flask, request


def create_app():
    app = Flask(__name__)
    # ketika creating Flask application
    # - initiate DB -> create SQLIte database di local
    # - create table Users
    # - create table Transactions
    # ....
    return app


app = create_app()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Endpoint + HTTP method = API
# /users + GET/POST/PUT/DELETE
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        return add_new_user()
    elif request.method == "GET":
        return get_current_users()


# Flask View Function
# Create API GET /user?name=...
@app.route("/user")
def specific_user():
    name = request.args.get("name")
    if name:
        return f"Username is {name}", 200
    else:
        return "User doesn't have any name", 400


@app.route("/login", methods=["POST"])
def login():
    pass


# Problem 1: Create API POST /login, yang specifikasinya a,b,c
# Probelm 2: Create API POST /users buat nambahin user baru
#   - body: {"name": ..., "age": ...}


def add_new_user(name=None, age=None):
    # TODO: tambahkan logic add user
    # - execute Insert SQL ke table user
    return "New user is added"


def get_current_users():
    # TODO: tambahkan get user
    return "Current users are fetched"
