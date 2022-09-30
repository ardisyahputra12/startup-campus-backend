from flask import Flask, current_app, request
from sqlalchemy import (
    Column,
    MetaData,
    Integer,
    Table,
    create_engine,
    text,
    insert,
    select,
    update,
)

import os


def get_engine():
    """Creating SQLite Engine to interact"""
    return create_engine("sqlite:///app2.db", future=True)


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


def create_app():
    app = Flask(__name__)

    # IMPLEMENT THIS
    # Keep track the amount of candies and chocolates throughout
    #   - Database (e.g. SQLite)
    # - create table to store information
    #   Table: money
    #    Column: amount (int)

    # remove database before creating app
    if os.path.isfile("app2.db"):
        os.remove("app2.db")
    print("Database is removed")

    engine = get_engine()
    # creating table money
    meta = MetaData()
    money_t = Table(
        "money",
        meta,
        Column("amo  unt", Integer, nullable=False),
    )
    meta.create_all(engine)

    # insert initial amount of money
    # run_query("INSERT INTO money VALUES(100000)", commit=True)
    # SQLALchemy Core
    run_query(insert(money_t).values({"amo  unt": 100000}), commit=True)

    print("App is created successfully")
    return app


app = create_app()


@app.route("/money", methods=["GET"])
def get_money():
    # data = run_query("SELECT * FROM money")
    # SQLAlchemy Core
    engine = get_engine()
    money_t = Table("money", MetaData(bind=engine), autoload=True)
    data = run_query(select([money_t.c["amo  unt"]]))

    money = data[0]["amo  unt"]
    return {"message": f"I have Rp {money}"}


@app.route("/spend", methods=["POST"])
def spend_money():
    body = request.json
    amount = body["amount"]

    # check current amount of money
    data = run_query("SELECT * FROM money")
    cur_money = data[0]["amo  unt"]

    if amount > cur_money:
        return {"error": "Insufficient fund"}, 403

    # updating amount of money
    remaining = cur_money - amount
    # run_query(f'UPDATE money SET "amo  unt" = {remaining}', commit=True)
    engine = get_engine()
    money_t = Table("money", MetaData(bind=engine), autoload=True)
    data = run_query(update(money_t).values({"amo  unt": remaining}), commit=True)

    return {"message": "Money is spent successfully"}


if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    initial_money_response = c.get("/money")
    assert initial_money_response.json == {"message": "I have Rp 100000"}
    assert initial_money_response.status_code == 200

    spend_money_response = c.post("/spend", json={"amount": 30000})
    assert spend_money_response.json == {"message": "Money is spent successfully"}
    assert spend_money_response.status_code == 200

    check_money_response = c.get("/money")
    assert check_money_response.json == {"message": "I have Rp 70000"}
    assert check_money_response.status_code == 200

    overspent_response = c.post("/spend", json={"amount": 85000})
    assert overspent_response.json == {"error": "Insufficient fund"}
    assert overspent_response.status_code == 403

    print("SUCCESS")
