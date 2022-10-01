"""
Registration.

There are two type of users in the marketplace:
- Seller: those who can stock and sell antique items
- Buyer: those who can view and purchase antique items

Before users can perform any activities, they first need to register. When registering, they
need to select between registering as "Seller" or "Buyer", and then input these info:
- username (required): unique identifier in the marketplace
- password: secure string to authenticate

You can't register with an existing username (across all sellers and buyers). If a 
seller/buyer hsa registered with a username U, then a future seller/buyer can't register 
with username U.

[Endpoint]

You need to implement the following endpoint:
- URL: /register
- Method: POST
- Request body
    - type: string (required) -> "Seller" or "Buyer"
    - username: string (required)
    - password: string (required)

Requirements (from the earliest to check):
- Password needs to satisfy certain standard:
    - each password will be checked (in this order) whether it:
        - contains >= 8 characters
        - contains >= 1 lowercase letter
        - contains >= upercase letter 
        - contains a number
    - if password is less than 8 characters:
        - return {"error": "Password must contain at least 8 characters"}
        - status code: 400
    - if password doesn't contain any lowercase letters:
        - return {"error": "Password must contain a lowercase letter"}
        - status code: 400
    - if password doesn't contain any uppercase letters:
        - return {"error": "Password must contain an uppercase letter"}
        - status code: 400
    - if password doesn't contain any numbers:
        - return {"error": "Password must contain a number"}
        - status code: 400
- When registering with an existing username:
    - return {"message": "Username <username> already exists"}
    - status code: 409
- If everything is valid:
    - record the new user in the database according to their type (seller/buyer)
    - if registering as a seller:
        - return {"message": "Congratulations, you can now sell antique items"}
        - status code: 201
    - if registering as a buyer:
        - return {"message": "Congratulations, you can now shop for antique items"}
        - status code: 201
"""
from flask import Blueprint

# this means that you can group all endpoints with prefix "/register" together
register_bp = Blueprint("register", __name__, url_prefix="/register")

# this means
@register_bp.route("", methods=["POST"])
def register():
    # IMPLEMENT THIS
    pass
