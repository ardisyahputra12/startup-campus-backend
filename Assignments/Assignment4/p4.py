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
