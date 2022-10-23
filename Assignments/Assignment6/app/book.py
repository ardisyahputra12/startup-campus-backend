from utils import get_engine, run_query
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)
from sqlalchemy.exc import IntegrityError


book_bp = Blueprint("book", __name__, url_prefix="/book")


@book_bp.route("", methods=["POST"])
def add_book():
    body = request.json
    title = body["title"]

    books = Table("books", MetaData(bind=get_engine()), autoload=True)
    try:
        run_query(insert(books).values({"title": title}), commit=True)
        return {"message": f"Book {title} is added"}, 201
    except IntegrityError:
        # case: when the book already exists
        return {"error": "Book with the same title already exists"}, 400


@book_bp.route("", methods=["GET"])
def get_books():
    books_t = Table("books", MetaData(bind=get_engine()), autoload=True)
    books = run_query(select([books_t.c.title, books_t.c.borrower]))
    return books


@book_bp.route("", methods=["DELETE"])
def delete_book():
    body = request.json
    title = body["title"]

    # check information about the book
    books = Table("books", MetaData(bind=get_engine()), autoload=True)
    book_details = run_query(select(books).where(books.c.title == title))

    # case; book doesn't exist
    if not book_details:
        return {"error": "Book is not known"}, 400

    # case: book is currently borrowed
    borrower = book_details[0]["borrower"]
    if borrower:
        return {"error": f"Book is currently borrowed by {borrower}"}, 403

    # remove book validly
    run_query(delete(books).where(books.c.title == title), commit=True)
    return {"message": f"Book {title} is removed"}
