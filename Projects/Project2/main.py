"""
Marketplace.

In this project, you are given a simple simulation of marketplace. You need to implement 
endpoints (instead of classes in Project 1).

Please check the following files for more detailed explanations (in this order):
    - Registration: register.py
    - Login: login.py
    - Seller: seller.py

TO DO:
    - Implement setup logic below (on create_app function)
    - Implement ALL the endpoints with IMPLEMENT THIS
    - You may optionally implement additional functions or classes as you see fit
    - Feel free to discuss the high-level ideas with your friend (but not the code)

DO NOT:
    - Remove any functions/methods/classes given to you
    - Import additional library outside of 
        - the standard Python library
        - installed libraries (via virtual environment)
    - Copy paste exact implementation from anyone
"""
from flask import Flask

from login import login_bp
from register import register_bp
from seller import seller_bp
from utils import COL


def create_app():
    app = Flask(__name__)

    # always register your blueprint(s) when creating application
    blueprints = [register_bp, login_bp, seller_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # IMPLEMENT THIS
    # - setup SQLite database (if already exists, clear/reset the database)
    # - create necessary tables

    return app


app = create_app()

# TEST IT YOURSELF
#   cd to Project2 folder
#   python3 main.py
#
# Note:
#   - this section only contains tests for registration process, but feel free to
#       add or modify if you want to test other endpoints
if __name__ == "__main__":
    from utils import assert_eq

    app.config.update({"TESTING": True})
    c = app.test_client()

    print(f"{COL.BOLD}Testing...{COL.ENDC}")

    # register seller
    register_seller_response = c.post(
        "/register",
        json={"type": "seller", "username": "A", "password": "Ab123456"},
    )
    assert_eq(
        register_seller_response.json,
        {"message": "Congratulations, you can now sell antique items"},
    )
    assert_eq(register_seller_response.status_code, 201)

    # register buyer
    register_buyer_response = c.post(
        "/register",
        json={"type": "buyer", "username": "B", "password": "Ab123456"},
    )
    assert_eq(
        register_buyer_response.json,
        {"message": "Congratulations, you can now shop for antique items"},
    )
    assert_eq(register_buyer_response.status_code, 201)

    # example for invalid password
    invalid_password_response = c.post(
        "/register",
        json={"type": "seller", "username": "C", "password": "ABZZCDZZ"},
    )
    assert_eq(
        invalid_password_response.json,
        {"error": "Password must contain a lowercase letter"},
    )
    assert_eq(invalid_password_response.status_code, 400)

    # can't re-register with the same username
    reregister_response = c.post(
        "/register",
        json={"type": "seller", "username": "B", "password": "654321bA"},
    )
    assert_eq(reregister_response.json, {"error": "Username B already exists"})
    assert_eq(reregister_response.status_code, 409)

    print(f"{COL.PASS}ALL TESTS ARE PASSED!{COL.ENDC}")
