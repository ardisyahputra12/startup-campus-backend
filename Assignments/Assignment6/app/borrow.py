from utils import get_engine, run_query
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError


borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")


@borrow_bp.route("", methods=["POST"])
def borrow_book():
    body = request.json
    name = body["name"]
    title = body["title"]

    # check information about the book
    books = Table("books", MetaData(bind=get_engine()), autoload=True)
    book_details = run_query(select(books).where(books.c.title == title))

    # case; book doesn't exist
    if not book_details:
        return {"error": "Book is not known"}, 400

    # check the borrower of this book
    borrower = book_details[0]["borrower"]
    if not borrower:
        run_query(
            update(books).where(books.c.title == title).values({"borrower": name}),
            commit=True,
        )
        return {"message": f"Book {title} is borrowed by {name}"}
    elif borrower != name:
        return {"error": f"Book is currently borrowed"}, 403
    elif borrower == name:
        return {"error": "You are currently borrowing this book"}, 400
