from sqlalchemy import Column, MetaData, String, Table, inspect
from sqlalchemy.exc import IntegrityError
from utils import get_engine
from flask import Flask

from book import book_bp
from borrow import borrow_bp
from return_book import return_bp


def create_app():
    app = Flask(__name__)

    engine = get_engine()
    if not inspect(engine).has_table("books"):
        meta = MetaData()
        Table(
            "books",
            meta,
            Column("title", String, nullable=False, unique=True),
            # for each book, we store information about who is currently borrowing this book
            # but allow the value to be None since the book can be in a non-borrowed state
            Column("borrower", String),
        )
        meta.create_all(engine)

    blueprints = [book_bp, borrow_bp, return_bp]

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


app = create_app()
app.run()
