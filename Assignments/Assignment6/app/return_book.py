from utils import get_engine, run_query
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    select,
    update,
)


return_bp = Blueprint("return", __name__, url_prefix="/return")


@return_bp.route("", methods=["POST"])
def return_book():
    body = request.json
    name = body["name"]
    title = body["title"]

    # check information about the book
    books = Table("books", MetaData(bind=get_engine()), autoload=True)
    book_details = run_query(select(books).where(books.c.title == title))

    if not book_details or book_details[0]["borrower"] != name:
        return {"error": "You never borrow book <title>"}, 400

    run_query(
        update(books).where(books.c.title == title).values({"borrower": None}),
        commit=True,
    )
    return {"message": f"Book {title} is returned safely"}
