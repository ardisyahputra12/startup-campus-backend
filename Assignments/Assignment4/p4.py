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
by a unique <username>.

[ADD NEW BOOK]

[[Endpoint]]
- Method: POST
- URL: /book
- Request body
    - title: string (required)

[[Logic]]
1. Librarian can add a new book (guaranteed to have a unique title)
    - return {"message": "Book <title> is added"}
    - status code; 201

[REMOVE A BOOK]

[[Endpoint]]
- Method: DELETE
- URL: /book
- Request body
    - title: string (required)

[[Logic]]
1. When a librarian validly removes an existing book:
    - remove the book from the collections in the library
    - return {"message": "Book <title> is added"}
    - status code; 201
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
    - title: string (required)

[[Logic]]
1. When a visitor validly borrows an existing book:
    - the book can't be borrowed by other visitors untul the book is returned
    - the book can't be removed by the librarian until the book is returned
    - return {"message": "Book <title> is borrowed by <username>"}
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

from flask import Flask


def create_app():
    app = Flask(__name__)

    # IMPLEMENT THESE:
    # - create a SQLite database
    # - create all required tables to store information regarding books and users
    raise NotImplementedError()

    return app


app = create_app()


##############################################################################################
# Helper Methods
##############################################################################################


# TEST IT YOURSELF
#   cd to Assignment4 folder
#   python3 p4.py
#
# please change the scenario as you wish
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    try:
        print("Testing p4.py DONE!")
    finally:
        # remove DB if already exists
        db_name = "p4.db"
        if os.path.isfile(db_name):
            os.remove(db_name)
