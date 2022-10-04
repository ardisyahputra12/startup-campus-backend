"""
Library.

In this problem, you need to implement endpoints that reflects the behavior in a library. 
The librarian can:
    - add a new book into the library
    - remove a book from the library

A visitor can:
    - borrow a book from the library
    - return a borrowed book to the library

All books will be represented by a unique <title>, while all visitors will be represented
by a unique <name>.

[ADD NEW BOOK]

[[Endpoint]]
- Method: POST
- URL: /book
- Request body
    - title: string (required)

[[Logic]]
1. Librarian can add a new book (or a book that has been removed):
    - return {"message": "Book <title> is added"}
    - status code; 201
2. If the book with the same title is already in the library (even if it's currently borrowed)
    - return {"error": "Book with the same title already exists"}
    - status code: 400

[REMOVE A BOOK]

[[Endpoint]]
- Method: DELETE
- URL: /book
- Request body
    - title: string (required)

[[Logic]]
1. When a librarian validly removes an existing book:
    - remove the book from the collections in the library
    - return {"message": "Book <title> is removed"}
    - status code; 200
2. If book with that title doesn't, or is no longer exist in the library:
    - return {"error": "Book is not known"}
    - status code: 400
3. If book with that title is currently borrowed by someone:
    - return {"error": "Book is currently borrowed by <name>"}
    - status code: 403

[BORROW]

[[Endpoint]]
- Method: POST
- URL: /borrow
- Request body
    - name: name of the visitor (required)
    - title: string (required)

[[Logic]]
1. When a visitor validly borrows an existing book:
    - the book can't be borrowed by other visitors untul the book is returned
    - the book can't be removed by the librarian until the book is returned
    - return {"message": "Book <title> is borrowed by <name>"}
    - status code; 200
2. If book with that title doesn't, or is no longer exist in the library:
    - return {"error": "Book is not known"}
    - status code: 400
3. If book with that title is currently borrowed by someone:
    - return {"error": "Book is currently borrowed"}
    - status code: 403
4. If book with that title is currently borrowed by this user:
    - return {"error": "You are currently borrowing this book"}
    - status code: 400
5. A visitor can borrow any number of books.

[RETURN]

[[Endpoint]]
- Method: POST
- URL: /return
- Request body
    - name: name of the visitor (required)
    - title: string (required)

[[Logic]]
1. When a visitor validly returns an existing book:
    - the book can now be borrowed (by other visitors) or removed (by librarian)
    - return {"message": "Book <title> is returned safely"}
    - status code; 200
2. If the user never actually borrows the book with the given title:
    - return {"error": "You never borrow book <title>"}
    - status code: 400
"""
import os
from flask import Flask, request
from sqlalchemy import Column, MetaData, String, Table, create_engine, text

db_name = "p4.db"
if os.path.isfile(db_name):
    os.remove(db_name)

def get_engine():
    """Creating SQLite Engine to interact"""
    return create_engine(f"sqlite:///{db_name}", future=True)


def create_app():
    app = Flask(__name__)

    # IMPLEMENT THESE:
    # - create a SQLite database
    # - create all required tables to store information regarding books and users
    # raise NotImplementedError()
    engine = get_engine()
    meta = MetaData()
    Table(
        "books",
        meta,
        Column("title", String, nullable=False, unique=True)
    )
    Table(
        "visitors",
        meta,
        Column("name", String, nullable=False),
        Column("title", String, nullable=False, unique=True)
    )
    meta.create_all(engine)

    return app


app = create_app()


def error_message(msg: str, sts: int):
    return {
        "error": msg
    }, sts

def success_message(msg: str, sts: int):
    return {
        "message": msg
    }, sts

@app.route("/book", methods=["POST"])
def add_new_book():
    data = request.get_json()
    # Request body:
    #     - title: string (required)
    books_title = run_query(f"SELECT title FROM books WHERE title = '{data['title']}'")

    if [{"title": data["title"]}] == books_title:
        return error_message("Book with the same title already exists", 400)
    else:
        run_query(f"INSERT INTO books VALUES ('{data['title']}')", commit=True)
        return success_message(f"Book {data['title']} is added", 201)

@app.route("/book", methods=["DELETE"])
def remove_book():
    data = request.get_json()
    # Request body:
    #     - title: string (required)
    visitors_name = run_query(f"SELECT name FROM visitors WHERE title = '{data['title']}'")
    visitors_title = run_query(f"SELECT title FROM visitors WHERE title = '{data['title']}'")
    books_title = run_query(f"SELECT title FROM books WHERE title = '{data['title']}'")

    if [{"title": data["title"]}] != books_title:
        return error_message("Book is not known", 400)
    elif [{"title": data["title"]}] == visitors_title:
        return error_message(f"Book is currently borrowed by {visitors_name[0]['name']}", 403)
    else:
        run_query(f"DELETE FROM books WHERE title='{data['title']}'", commit=True)
        return success_message(f"Book {data['title']} is removed", 200)


@app.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json()
    # Request body:
    #     - name: name of the visitor (required)
    #     - title: string (required)
    books_title = run_query(f"SELECT title FROM books WHERE title = '{data['title']}'")
    visitors_title_name = run_query(f"SELECT title FROM visitors WHERE title = '{data['title']}' AND name = '{data['name']}'")
    visitors_title = run_query(f"SELECT title FROM visitors WHERE title = '{data['title']}'")

    if [{"title": data["title"]}] != books_title:
        return error_message("Book is not known", 400)
    elif [{"title": data["title"]}] == visitors_title_name:
        return error_message("You are currently borrowing this book", 400)
    elif [{"title": data["title"]}] == visitors_title:
        return error_message("Book is currently borrowed", 403)
    else:
        run_query(f"INSERT INTO visitors VALUES {data['name'], data['title']}", commit=True)
        return success_message(f"Book {data['title']} is borrowed by {data['name']}", 200)

@app.route("/return", methods=["POST"])
def return_book():
    data = request.get_json()
    # Request body:
    #     - name: name of the visitor (required)
    #     - title: string (required)
    visitors_name = run_query(f"SELECT name FROM visitors WHERE title = '{data['title']}'")
    visitors_title = run_query(f"SELECT title FROM visitors WHERE title = '{data['title']}'")

    if [{"name": data["name"]}] != visitors_name:
        return error_message(f"You never borrow book {visitors_title[0]['title']}", 400)
    else:
        run_query(f"DELETE FROM visitors WHERE title='{data['title']}'", commit=True)
        return success_message(f"Book {visitors_title[0]['title']} is returned safely", 200)


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
#   python3 p4.py
#
# please change the scenario as you wish
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    # adding 2 books to the library
    add_book1_response = c.post("/book", json={"title": "Cooking for Dummies"})
    assert add_book1_response.json == {"message": "Book Cooking for Dummies is added"}
    assert add_book1_response.status_code == 201
    add_book2_response = c.post("/book", json={"title": "Advanced Python"})
    assert add_book2_response.json == {"message": "Book Advanced Python is added"}
    assert add_book2_response.status_code == 201

    # a visitor borrows the 1st book
    borrow_response = c.post(
        "/borrow", json={"name": "Michael", "title": "Cooking for Dummies"}
    )
    assert borrow_response.json == {
        "message": "Book Cooking for Dummies is borrowed by Michael"
    }
    assert borrow_response.status_code == 200

    # librarian can't remove the 1st book
    remove_response = c.delete("/book", json={"title": "Cooking for Dummies"})
    assert remove_response.json == {"error": "Book is currently borrowed by Michael"}
    assert remove_response.status_code == 403

    # 2nd visitor can't borrow the 1st book
    borrow2_response = c.post(
        "/borrow", json={"name": "Jude", "title": "Cooking for Dummies"}
    )
    assert borrow2_response.json == {"error": "Book is currently borrowed"}
    assert borrow2_response.status_code == 403

    # 1st visitor returns the 1st book
    return_response = c.post(
        "/return", json={"name": "Michael", "title": "Cooking for Dummies"}
    )
    assert return_response.json == {
        "message": "Book Cooking for Dummies is returned safely"
    }
    assert return_response.status_code == 200

    # 2nd visitor can now borrow the 1st book
    borrow3_response = c.post(
        "/borrow", json={"name": "Jude", "title": "Cooking for Dummies"}
    )
    assert borrow3_response.json == {
        "message": "Book Cooking for Dummies is borrowed by Jude"
    }
    assert borrow3_response.status_code == 200

    # librarian removes the 2nd book
    remove2_response = c.delete("/book", json={"title": "Advanced Python"})
    assert remove2_response.json == {"message": "Book Advanced Python is removed"}
    assert remove2_response.status_code == 200

    print("Testing p4.py DONE!")
