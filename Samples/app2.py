"""
Tracking pengeluaran.

Awalnya punya uang = 100,000

Kita bisa melakukan 2 hal
1. check total uang saat ini
2. mengeluarkan uang

[Check total uang]
Endpoint:
  - URL: /money
  - Method: GET
Logic
  - get the amount of money currently
    - return {"message": "I have Rp <amount_of_money>"}
    - status code: 200

[Spend]
Endpoints:
  - URL: /spend
  - Method: POST
  - Request body:
      - amount: integer
Logic:
  - spend "amount" from current money
    - return {"message": "Money is spent successfully"}
    - status code: 200
  - if "amount" is bigger than current # of money
    - return {"error": "Insufficient fund"}
    - status code: 403
"""
from flask import Flask, current_app, request


def create_app():
    app = Flask(__name__)

    # IMPLEMENT THIS
    # Keep track the amount of candies and chocolates throughout
    # HINT: you can use:
    #   - Database (e.g. SQLite)
    #   - Use app.config[<key>] to store value and current_app.config[<key>] to retrieve
    app.config["money"] = 100000
    # similar to storing variable in dict -> {"money": 100000}

    return app


app = create_app()
# can we use global variable?
# MONEY = 100000


@app.route("/money", methods=["GET"])
def get_money():
    # money = MONEY
    # print(f"Money <get_money>: {money}")
    money = current_app.config["money"]
    return {"message": f"I have Rp {money}"}


@app.route("/spend", methods=["POST"])
def spend_money():
    body = request.json
    amount = body["amount"]
    cur_money = current_app.config["money"]
    # global MONEY
    # cur_money = MONEY

    # case: amount > cur_money
    if amount > cur_money:
        return {"error": "Insufficient fund"}, 403

    # calculate remaining amount of money
    remaining = cur_money - amount
    # set remaining amount of money to current_app.config
    current_app.config["money"] = remaining
    # MONEY = remaining

    return {"message": "Money is spent successfully"}


if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    # Contoh bahwa current_app tidak bisa digunakan di luar endpoint logic
    # print("MONEY", current_app.config["money"])

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
