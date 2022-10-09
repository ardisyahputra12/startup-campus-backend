"""
Seller.

A seller can do one of the following things:
    - Stock specific amount of an item (to be sold in the market)
    - Update the amount/price of an item
    - Access current revenue

Note that each item is identified by a UNIQUE name per SELLER (different sellers can sell
items with the same name - seller A and B can sell item X)

Implement these actions with the following endpoints:

[Stock new item]
- URL: /seller/stock
- method: POST
- Request body:
    - item: string (required) -> name of this item
    - amount: integer (required) -> how many items to stock
    - price: integer (required) -> unit price (price per individual item)
- Headers:
    - token: string (required) -> token obtained from login to identify this seller

Requirements (from the earliest to check):
- If amount is not a positive number:
    - return {"error": "Please specify a positive amount"}
    - status code: 400
- If price is is not a positive number:
    - return {"error": "Please specify a positive amount"}
    - status code: 400
- If token does not identify a seller:
    - return {"error": "Unauthorized seller"}
    - status code: 403
- If the same item (name) has been previously stocked:
    - return {"error": "Item with the same name already exists"}
    - status code: 400
- Else, everything is valid:
    - Add <amount> of this item to the stock
    - return {"message": "Stocking successful"}
    - status code: 201

[Update amount OR price]
- URL: /seller/stock
- method: PUT
- Request body:
    - item: string (required) -> name of item to update
    - amount: integer (optional) -> the new stock for this item
    - price: integer (optional) -> unit price (price per individual item)
- Headers:
    - token: string (required) -> token obtained from login to identify this seller

Requirements (from the earliest to check):
- If both amount and price are not given
    - return {"error": "Please specify amount or price"}
    - status code: 400
- If price is GIVEN and is not a positive number:
    - return {"error": "Please specify a positive amount"}
    - status code: 400
- If amount is GIVEN and is a negative number:
    - return {"error": "Please specify a positive amount OR 0"}
    - status code: 400
- If token does not identify a seller:
    - return {"error": "Unauthorized seller"}
    - status code: 403
- If seller never stocks this item:
    - return {"error": "Item is not known"}
    - status code: 400
- Else, everything is valid:
    - Update the given price/amount of the is item
    - return {"message": "Item information is updated"}
    - status code: 200

[Get revenue]
- URL: /seller/revenue
- method: GET
- Headers:
    - token: string (required) -> token obtained from login to identify this seller

Requirements (from the earliest to check):
- If token does not identify a seller:
    - return {"error": "Unauthorized seller"}
    - status code: 403
- If everything is valid:
    - calculate revenue by the total price of items sold by this seller (so far)
        - initially, sellers' revenue is 0 (as they have not sold anything yet)
    - return {"message": "Your revenue is <revenue>"}
    - status code: 200
"""
from flask import Blueprint, request
from utils import run_query, error_message, success_message

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")

# Requirements (from the earliest to check):
# - If amount is not a positive number:
#     - return {"error": "Please specify a positive amount"}
#     - status code: 400
# - If price is is not a positive number:
#     - return {"error": "Please specify a positive amount"}
#     - status code: 400
# - If token does not identify a seller:
#     - return {"error": "Unauthorized seller"}
#     - status code: 403
# - If the same item (name) has been previously stocked:
#     - return {"error": "Item with the same name already exists"}
#     - status code: 400
# - Else, everything is valid:
#     - Add <amount> of this item to the stock
#     - return {"message": "Stocking successful"}
#     - status code: 201
@seller_bp.route("/stock", methods=["POST"])
def add_stock():
    # IMPLEMENT THIS
    header = request.headers
    data = request.get_json()
    # - Request body:
    #     - item: string (required) -> name of this item
    #     - amount: integer (required) -> how many items to stock
    #     - price: integer (required) -> unit price (price per individual item)
    # - Headers:
    #     - token: string (required) -> token obtained from login to identify this seller
    # print("="*20)
    # print(run_query(f"SELECT username, token FROM users WHERE token = '{header['Token']}'"))
    # print([{"item": data["item"]}])
    # print("="*20)
    # print(run_query(f"SELECT item FROM stock WHERE item = '{data['item']}'"))

    # if [{"token": header["Token"]}] != run_query(f"SELECT token FROM users WHERE token = '{header['Token']}'"):
    #     return error_message("Unauthorized seller", 403)
    if (data["amount"] < 1) or (data["price"] < 1):
        return error_message("Please specify a positive amount", 400)
    if [{"item": data["item"]}] == run_query(f"SELECT item FROM stock WHERE item = '{data['item']}'"):
        return error_message("Item with the same name already exists", 400)
    else:
        run_query(f"INSERT INTO stock VALUES {data['item'], data['amount'], data['price']}", commit=True)
        return success_message("Stocking successful", 201)


@seller_bp.route("/stock", methods=["PUT"])
def update_stock():
    # IMPLEMENT THIS
    pass


@seller_bp.route("/revenue", methods=["GET"])
def revenue():
    # IMPLEMENT THIS
    pass
