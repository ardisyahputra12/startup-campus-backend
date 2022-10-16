"""
Buyer.

A buyer can do one of the following things:
    - View the unit price of an item (price per individual item)
    - Add a number of specific item to a basket (max. 1 basket per buyer)
    - Remove (all amount of) specific item from the basket 
    - Top up balance
    - Pay (for all items in the basket)

Buyers have a basket that can store items, and when they decide to pay they pay for the whole
basket. Buyers have the opportunity to adjust the basket (add new items / adjust number of 
items) accordingly before making any payment.

A buyer initially has 0 balance. He/she needs to top up sufficient balance before being able
to pay for the items in the basket. All successful payment will go to the revenue of each
seller. After a successful purchase, the basket is immediately cleared from all items.

Implement these actions with the following endpoints:

[View item]
- URL: /buyer/item?item={item}&seller={seller}
- method: GET
- Query parameters:
    - item: string (required) -> name of an item
    - seller: string (required) -> name of the seller selling this item
- Headers:
    - token: string (required) -> token obtained from login to identify this buyer

Requirements (from the earliest to check):
- If token does not identify a buyer:
    - return {"error": "Unauthorized buyer"}
    - status code: 403
- If seller never stocks this item:
    - return {"error": "Item is not known"}
    - status code: 400
- Else, everything is valid:
    - return {"message": "Price is <price>"}
    - status code: 200
- NOTE:
    - If seller runs out of stock of an item, buyers can still view the item's price
    - Price of an item should be the most updated (e.g. if the seller just updated an item's
        price, then buyers should be able to see that price through this endpoint)

[Add item to the basket]
- URL: /buyer/item
- method: POST
- Request body:
    - item: string (required) -> name of an item
    - seller: string (required) -> name of the seller selling this item
    - amount: integer (required) -> how many of this item to add to the basket
- Headers:
    - token: string (required) -> token obtained from login to identify this buyer

Requirements (from the earliest to check):
- If amount is not a positive number:
    - return {"error": "Please specify a positive amount"}
    - status code: 400
- If token does not identify a buyer:
    - return {"error": "Unauthorized buyer"}
    - status code: 403
- If seller never stocks this item:
    - return {"error": "Item is not known"}
    - status code: 400
- Else, everything is valid:
    - return {"message": "Item is added to the basket"}
    - status code: 201
- NOTE:
    - when an item has been previously added to a basket, user can add more copies of 
        the item (e.g. B adds 3 item I, then adds another 5 => B now have 8x I in the basket)
    - when adding certain of item to the basket, no need to check whether the seller has 
        that many in stock (checking only happens when buying)

[Remove item from basket]
- URL: /buyer/item
- method: DELETE
- Request body:
    - item: string (required) -> name of an item
    - seller: string (required) -> name of the seller selling this item
- Headers:
    - token: string (required) -> token obtained from login to identify this buyer

Requirements (from the earliest to check):
- If token does not identify a buyer:
    - return {"error": "Unauthorized buyer"}
    - status code: 403
- If buyer never adds this item to the basket:
    - return {"error": "Item is not in the basket"}
    - status code: 400
- Else, everything is valid:
    - return {"message": "Item is removed from the basket"}
    - status code: 200

[Top up]
- URL: /buyer/topup
- method: POST
- Request body:
    - amount: string (required) -> the amount of money to add to the balance
- Headers:
    - token: string (required) -> token obtained from login to identify this buyer

Requirements (from the earliest to check):
- If amount is not a positive number:
    - return {"error": "Please specify a positive amount"}
    - status code: 400
- If token does not identify a buyer:
    - return {"error": "Unauthorized buyer"}
    - status code: 403
- Else, everything is valid:
    - Top up <amount> to the buyer's balance
    - return {"message": "Your balance is updated"}
    - status code: 200

[Pay]
- URL: /buyer/pay
- method: POST
- Headers:
    - token: string (required) -> token obtained from login to identify this buyer

Requirements (from the earliest to check):
- If token does not identify a buyer:
    - return {"error": "Unauthorized buyer"}
    - status code: 403
- When the basket is empty:
    - return {"error": "Basket is empty"}
    - status code: 400
- If amount of an item in the basket is less than the stock in the seller
    - return {"error": "Insufficient stock"}
    - status code: 400
- If the total price of the basket is greater than the buyer's balance:
    - return {"error": "Please top up <diff>"}
        where <diff> is he difference between buyer's balance and total price of the basket
    - status code: 400
- Else, everything is valid:
    - Subtract the total price from the buyer's balance
    - Add revenue to corresponding seller (based on the price of bought items)
    - Subtract the stock of each bought item from each seller's stock
    - Clear all items from the buyer's basket
    - return {"message": "Payment is successsful"}
    - status code: 200
"""
from flask import Blueprint, request
from utils import run_query, error_message, success_message

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")


@buyer_bp.route("/item", methods=["GET"])
def view_item():
    # IMPLEMENT THIS
    params = request.args
    token = request.headers["Token"]
    item = params.get("item", type=str)
    seller = params.get("seller", type=str)

    if run_query(f"SELECT token FROM users WHERE token = '{token}' AND type = 'buyer'") == []:
        return error_message("Unauthorized buyer", 403)
    elif run_query(f"SELECT item FROM stock INNER JOIN users ON users.token=stock.token WHERE item = '{item}' AND username = '{seller}'") == []:
        return error_message("Item is not known", 400)
    else:
        price = run_query(f"SELECT price FROM stock INNER JOIN users ON users.token=stock.token WHERE item='{item}' AND username = '{seller}'")[0]["price"]
        return success_message(f"Price is {price}", 200)


@buyer_bp.route("/item", methods=["POST"])
def add_item():
    # IMPLEMENT THIS
    data = request.get_json()
    token = request.headers["Token"]

    if data["amount"] < 1:
        return error_message("Please specify a positive amount", 400)
    elif run_query(f"SELECT token FROM users WHERE token = '{token}' AND type = 'buyer'") == []:
        return error_message("Unauthorized buyer", 403)
    elif run_query(f"SELECT item FROM stock WHERE item = '{data['item']}'") == []:
        return error_message("Item is not known", 400)
    else:
        if [{"item": data["item"]}] == run_query(f"SELECT item FROM basket WHERE item = '{data['item']}' AND seller = '{data['seller']}' AND token = '{token}'"):
            run_query(f"UPDATE basket SET amount = amount + '{data['amount']}' WHERE item = '{data['item']}' AND seller = '{data['seller']}' AND token = '{token}'", commit=True)
        else:
            run_query(f"INSERT INTO basket VALUES {data['seller'], data['item'], data['amount'], token}", commit=True)
        return success_message("Item is added to the basket", 201)


@buyer_bp.route("/item", methods=["DELETE"])
def remove_item():
    # IMPLEMENT THIS
    data = request.get_json()
    token = request.headers["Token"]

    if run_query(f"SELECT token FROM users WHERE token = '{token}' AND type = 'buyer'") == []:
        return error_message("Unauthorized buyer", 403)
    elif run_query(f"SELECT item FROM basket WHERE item = '{data['item']}'") == []:
        return error_message("Item is not in the basket", 400)
    else:
        run_query(f"DELETE FROM basket WHERE item = '{data['item']}' AND seller = '{data['seller']}' AND token = '{token}'", commit=True)
        return success_message("Item is removed from the basket", 200)


@buyer_bp.route("/topup", methods=["POST"])
def topup():
    # IMPLEMENT THIS
    amount = request.get_json()["amount"]
    token = request.headers["Token"]

    if amount < 1:
        return error_message("Please specify a positive amount", 400)
    elif run_query(f"SELECT token FROM users WHERE token = '{token}' AND type = 'buyer'") == []:
        return error_message("Unauthorized buyer", 403)
    else:
        run_query(f"UPDATE users SET balance = '{amount}' WHERE token = '{token}' AND type = 'buyer'", commit=True)
        return success_message("Your balance is updated", 200)


@buyer_bp.route("pay", methods=["POST"])
def pay():
    # IMPLEMENT THIS
    token = request.headers["Token"]
    baskets = run_query(f"SELECT * FROM basket WHERE token = '{token}'")
    buyer_balance = run_query(f"SELECT balance FROM users WHERE token = '{token}'")
    total_price_basket = 0

    if run_query(f"SELECT token FROM users WHERE token = '{token}' AND type = 'buyer'") == []:
        return error_message("Unauthorized buyer", 403)
    elif run_query(f"SELECT seller FROM basket WHERE token = '{token}'") == []:
        return error_message("Basket is empty", 400)
    for basket in baskets:
        stocks = run_query(f"SELECT * FROM stock WHERE item = '{basket['item']}'")
        for stock in stocks:
            if [{"username": basket["seller"]}] == run_query(f"SELECT username FROM users WHERE token = '{stock['token']}'"):
                total = stock["price"] * basket["amount"]
                total_price_basket += total
    for basket in baskets:
        stocks = run_query(f"SELECT * FROM stock WHERE item = '{basket['item']}'")
        for stock in stocks:
            if [{"username": basket["seller"]}] == run_query(f"SELECT username FROM users WHERE token = '{stock['token']}'"):
                if (basket["amount"] > stock["amount"]):
                    return error_message("Insufficient stock", 400)
                elif total_price_basket > int(buyer_balance[0]["balance"]):
                    diff = total_price_basket - int(buyer_balance[0]["balance"])
                    return error_message(f"Please top up {diff}", 400)
                else:
                    run_query(f"UPDATE users SET balance = balance + ({stock['price'] * basket['amount']}) WHERE username = '{basket['seller']}' AND token = '{stock['token']}'", commit=True)
                    run_query(f"UPDATE stock SET amount = amount - {basket['amount']} WHERE item = '{basket['item']}' AND token = '{stock['token']}'", commit=True)
    run_query(f"UPDATE users SET balance = balance - {total_price_basket} WHERE token = '{token}'", commit=True)
    run_query(f"DELETE FROM basket WHERE token = '{token}'", commit=True)
    return success_message("Payment is successsful", 200)
