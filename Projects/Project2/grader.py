"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
import traceback
from functools import wraps
from random import choice, choices, randint, shuffle
from string import ascii_lowercase, ascii_uppercase, digits

##############################################################################################
# Helpers
##############################################################################################


def grade(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
        print("-" * 100)
        print(f.__name__)
        print("-" * 100)
        global MAX_SCORE, FINAL_SCORE
        MAX_SCORE, FINAL_SCORE = 0, 0
        try:
            f(*args, **kwargs)
        finally:
            res = FINAL_SCORE, MAX_SCORE
            # reset final score before returning
            FINAL_SCORE = 0
            return res

    return dec


def assert_eq_dict(expression, expected: dict) -> bool:
    if not isinstance(expression, dict):
        return False

    for k in expected:
        if k not in expression:
            return False

    for k, v in expression.items():
        if k not in expected:
            return False
        if v != expected[k]:
            return False

    return True


def assert_eq(
    expression, expected, exc_type=AssertionError, hide: bool = False, err_msg=None
):
    try:
        if isinstance(expected, dict):
            if assert_eq_dict(expression, expected):
                return
        elif expression == expected:
            return

        errs = [err_msg] if err_msg else []
        if hide:
            expected = "<hidden>"
        err = "\n".join([*errs, f"> Expected: {expected}", f"> Yours: {expression}"])
        raise exc_type(err)
    except Exception:
        raise


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
class COL:
    PASS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"


# special exception when something should've been printed, but wasn't
class DisplayError(Exception):
    pass


class Scorer:
    def __enter__(self):
        pass

    def __init__(self, score: int, desc: str):
        self.score = score
        global MAX_SCORE
        MAX_SCORE += score
        print(f"{COL.BOLD}{desc}{COL.ENDC} ({self.score} pts)")

    def __exit__(self, exc_type, exc_value, exc_tb):
        # add maximum score when passing these statements, otherwise 0
        if not exc_type:
            global FINAL_SCORE
            FINAL_SCORE += self.score
            print(COL.PASS, f"\tPASS: {self.score} pts", COL.ENDC)
        else:
            err_lines = [exc_type.__name__, *str(exc_value).split("\n")]
            errs = [
                "\t" + (" " * 4 if index else "") + line
                for index, line in enumerate(err_lines)
            ]
            print("{}{}".format(COL.WARNING, "\n".join(errs)))
            print(f"\t{COL.FAIL}FAIL: 0 pts", COL.ENDC)

        # skip throwing the exception
        return True


class safe_init:
    def __enter__(self):
        pass

    def __init__(self, max_score: int):
        self.max_score = max_score

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(traceback.format_exc())
            global MAX_SCORE
            MAX_SCORE = self.max_score
            return False

        return True


##############################################################################################
# Actual Tests
##############################################################################################


def assert_response(
    c,
    method: str,
    endpoint: str,
    json: dict = None,
    exp_json=None,
    exp_code: int = None,
    headers: dict = None,
):
    if not headers:
        headers = {}

    response = getattr(c, method)(endpoint, json=json, headers=headers)
    assert_eq(response.json, exp_json)
    assert_eq(response.status_code, exp_code)
    return response.json


def gen_password():
    # representative from each
    num = choice(digits)
    lower = choice(ascii_lowercase)
    upper = choice(ascii_uppercase)
    remaining = choices(
        [*digits, *ascii_lowercase, *ascii_uppercase], k=5 + randint(0, 5)
    )

    all_chars = [num, lower, upper, *remaining]
    shuffle(all_chars)
    res = "".join(all_chars)
    return res


class IsString:
    def __eq__(self, other):
        return isinstance(other, str)

    def __repr__(self):
        return "<must_be_a_string>"


@grade
def test_end_to_end():
    with safe_init(100):
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    sellers = [("Rio", gen_password()), ("Leo Nardo", gen_password())]
    with Scorer(2, "Registering new sellers"):
        for name, password in sellers:
            assert_response(
                c,
                "post",
                "/register",
                json={"type": "seller", "username": name, "password": password},
                exp_json={"message": "Congratulations, you can now sell antique items"},
                exp_code=201,
            )

    buyers = [
        ("Mary-Geoffe", gen_password()),
        ("Aryo Setioso", gen_password()),
        ("Theodore", gen_password()),
    ]
    with Scorer(2, "Registering new buyers"):
        for name, password in buyers:
            assert_response(
                c,
                "post",
                "/register",
                json={"type": "buyer", "username": name, "password": password},
                exp_json={
                    "message": "Congratulations, you can now shop for antique items"
                },
                exp_code=201,
            )

    with Scorer(6, "Check for invalid password"):
        invalid_passwords = [
            ("aB12cD3", "Password must contain at least 8 characters"),
            ("0123456", "Password must contain at least 8 characters"),
            ("AB12CD34", "Password must contain a lowercase letter"),
            ("ABZZCDZZ", "Password must contain a lowercase letter"),
            ("00120034", "Password must contain a lowercase letter"),
            ("ab12cd34", "Password must contain an uppercase letter"),
            ("ababcdcd", "Password must contain an uppercase letter"),
            ("aBBacDDc", "Password must contain a number"),
        ]
        for password, err_msg in invalid_passwords:
            name = choice(
                ["Hackerz", *[e[0] for e in sellers], *[e[0] for e in buyers]]
            )
            assert_response(
                c,
                "post",
                "/register",
                json={"type": "buyer", "username": name, "password": password},
                exp_json={"error": err_msg},
                exp_code=400,
            )

    with Scorer(4, "Can't register duplicate users"):
        for name, password in [*buyers, *sellers]:
            for type in ("seller", "buyer"):
                assert_response(
                    c,
                    "post",
                    "/register",
                    json={"type": type, "username": name, "password": password},
                    exp_json={"error": f"Username {name} already exists"},
                    exp_code=409,
                )

    with Scorer(2, "Successful login"):
        seller_tokens = []
        for name, password in sellers:
            response = assert_response(
                c,
                "post",
                "/login",
                json={"username": name, "password": password},
                exp_json={"message": "Welcome to the marketplace", "token": IsString()},
                exp_code=200,
            )
            seller_tokens.append(response["token"])

        buyer_tokens = []
        for name, password in buyers:
            response = assert_response(
                c,
                "post",
                "/login",
                json={"username": name, "password": password},
                exp_json={"message": "Welcome to the marketplace", "token": IsString()},
                exp_code=200,
            )
            buyer_tokens.append(response["token"])

    with Scorer(3, "Login by non-existent users"):
        for name in ("Hackerz", "Robin", "Trevor"):
            assert_response(
                c,
                "post",
                "/login",
                json={"username": name, "password": password},
                exp_json={"error": "Username or password is incorrect"},
                exp_code=401,
            )

    with Scorer(3, "Incorrect password when logging in"):
        valid_password = "aB123456"
        assert_response(
            c,
            "post",
            "/login",
            json={"username": sellers[0][0], "password": valid_password},
            exp_json={"error": "Username or password is incorrect"},
            exp_code=401,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": sellers[1][0], "password": None},
            exp_json={"error": "Username or password is incorrect"},
            exp_code=401,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": buyers[0][0], "password": valid_password},
            exp_json={"error": "Username or password is incorrect"},
            exp_code=401,
        )
        assert_response(
            c,
            "post",
            "/login",
            json={"username": buyers[1][0], "password": None},
            exp_json={"error": "Username or password is incorrect"},
            exp_code=401,
        )

    with Scorer(2, "Stocking new items successfully"):
        seller1_initial_items = [
            ("A1", 5, 10),
            ("A2", 5, 20),
            ("A3", 2, 150),
            ("B1", 5, 25),
            ("B2", 3, 50),
            ("B3", 1, 150),
        ]
        for item, amount, price in seller1_initial_items:
            assert_response(
                c,
                "post",
                "/seller/stock",
                json={"item": item, "amount": amount, "price": price},
                headers={"token": seller_tokens[0]},
                exp_json={"message": "Stocking successful"},
                exp_code=201,
            )

        seller2_initial_items = [
            ("A1", 5, 10),
            ("A2", 3, 25),
            ("A3", 2, 100),
            ("B1", 5, 20),
            ("B2", 1, 100),
            ("B3", 1, 250),
        ]
        for item, amount, price in seller2_initial_items:
            assert_response(
                c,
                "post",
                "/seller/stock",
                json={"item": item, "amount": amount, "price": price},
                headers={"token": seller_tokens[1]},
                exp_json={"message": "Stocking successful"},
                exp_code=201,
            )

    with Scorer(2, "Amount and price of item to stock must be positive"):
        for X in (-10, -5, 0):
            assert_response(
                c,
                "post",
                "/seller/stock",
                json={"item": "A4", "amount": X, "price": 123},
                headers={"token": seller_tokens[0]},
                exp_json={"error": "Please specify a positive amount"},
                exp_code=400,
            )
            assert_response(
                c,
                "post",
                "/seller/stock",
                json={"item": "A4", "amount": 10, "price": X},
                headers={"token": seller_tokens[1]},
                exp_json={"error": "Please specify a positive amount"},
                exp_code=400,
            )

    with Scorer(2, "Non-existent seller can't stock new item"):
        assert_response(
            c,
            "post",
            "/seller/stock",
            json={"item": "A4", "amount": 10, "price": 10},
            headers={"token": "123456"},
            exp_json={"error": "Unauthorized seller"},
            exp_code=403,
        )

    with Scorer(3, "Seller can't stock the same item (only update amount)"):
        assert_response(
            c,
            "post",
            "/seller/stock",
            json={"item": "A1", "amount": 10, "price": 10},
            headers={"token": seller_tokens[0]},
            exp_json={"error": "Item with the same name already exists"},
            exp_code=400,
        )

    with Scorer(3, "Seller can update amount/price of an item"):
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "B1", "amount": 10},
            headers={"token": seller_tokens[0]},
            exp_json={"message": "Item information is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A1", "amount": 10, "price": 12},
            headers={"token": seller_tokens[1]},
            exp_json={"message": "Item information is updated"},
            exp_code=200,
        )

    with Scorer(2, "Checking initial revenue"):
        for index, seller in enumerate(sellers):
            token = seller_tokens[index]
            assert_response(
                c,
                "get",
                "/seller/revenue",
                headers={"token": token},
                exp_json={"message": "Your revenue is 0"},
                exp_code=200,
            )

    with Scorer(2, "Non-existent seller can't check revenue"):
        for token in [*buyer_tokens, "123456"]:
            assert_response(
                c,
                "get",
                "/seller/revenue",
                headers={"token": token},
                exp_json={"error": "Unauthorized seller"},
                exp_code=403,
            )

    with Scorer(2, "Amount and price are not specified"):
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A4"},
            headers={"token": seller_tokens[1]},
            exp_json={"error": "Please specify amount or price"},
            exp_code=400,
        )

    with Scorer(2, "Amount of item to update must be non-negative"):
        for X in (-10, -5):
            assert_response(
                c,
                "put",
                "/seller/stock",
                json={"item": "A1", "amount": X, "price": 123},
                headers={"token": seller_tokens[0]},
                exp_json={"error": "Please specify a positive amount OR 0"},
                exp_code=400,
            )

    with Scorer(2, "Price of item to update must be positive"):
        for X in (-10, -5, 0):
            assert_response(
                c,
                "put",
                "/seller/stock",
                json={"item": "A1", "amount": 10, "price": X},
                headers={"token": seller_tokens[1]},
                exp_json={"error": "Please specify a positive amount"},
                exp_code=400,
            )

    with Scorer(2, "Non-existent seller can't update price"):
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A1", "amount": 10, "price": 10},
            headers={"token": "123456"},
            exp_json={"error": "Unauthorized seller"},
            exp_code=403,
        )

    with Scorer(4, "Can't update non-existent item"):
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A4", "amount": 10},
            headers={"token": seller_tokens[0]},
            exp_json={"error": "Item is not known"},
            exp_code=400,
        )

    with Scorer(4, "Buyer can view the price of items"):
        items = [
            ("A1", sellers[0][0], 10),
            ("A3", sellers[0][0], 150),
            ("B2", sellers[0][0], 50),
            ("B3", sellers[0][0], 150),
            ("A1", sellers[1][0], 12),
            ("A2", sellers[1][0], 25),
            ("B1", sellers[1][0], 20),
            ("B3", sellers[1][0], 250),
        ]
        for item in items:
            random_buyer_token = choice(buyer_tokens)
            assert_response(
                c,
                "get",
                f"/buyer/item?item={item[0]}&seller={item[1]}",
                headers={"token": random_buyer_token},
                exp_json={"message": f"Price is {item[2]}"},
                exp_code=200,
            )

    with Scorer(3, "Buyer can view updated prices"):
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "B1", "amount": 10},
            headers={"token": seller_tokens[0]},
            exp_json={"message": "Item information is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "get",
            f"/buyer/item?item=A1&seller={sellers[0][0]}",
            headers={"token": buyer_tokens[0]},
            exp_json={"message": f"Price is 10"},
            exp_code=200,
        )
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A1", "amount": 10, "price": 12},
            headers={"token": seller_tokens[1]},
            exp_json={"message": "Item information is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "get",
            f"/buyer/item?item=A1&seller={sellers[1][0]}",
            headers={"token": buyer_tokens[1]},
            exp_json={"message": f"Price is 12"},
            exp_code=200,
        )

    with Scorer(2, "Non-existent buyer can't view items"):
        for token in [*seller_tokens, "12345678"]:
            assert_response(
                c,
                "get",
                f"/buyer/item?item=A1&seller={sellers[0][0]}",
                headers={"token": token},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )
            assert_response(
                c,
                "get",
                f"/buyer/item?item=B2&seller={sellers[1]}",
                headers={"token": token},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )

    with Scorer(2, "Can't view non-existent items"):
        for seller in sellers:
            assert_response(
                c,
                "get",
                f"/buyer/item?item=A4&seller={seller[0]}",
                headers={"token": buyer_tokens[0]},
                exp_json={"error": "Item is not known"},
                exp_code=400,
            )

    with Scorer(2, "Succesfully adding items to the basket"):
        basket1_items = (
            ("A1", sellers[0][0], 4),
            ("A2", sellers[0][0], 3),
            ("A1", sellers[0][0], 3),
            ("B2", sellers[0][0], 3),
        )
        for item, seller, amount in basket1_items:
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": buyer_tokens[0]},
                json={"item": item, "seller": seller, "amount": amount},
                exp_json={"message": "Item is added to the basket"},
                exp_code=201,
            )

        basket2_items = (
            ("A1", sellers[1][0], 5),
            ("A2", sellers[1][0], 2),
            ("B2", sellers[1][0], 1),
            ("A2", sellers[1][0], 1),
        )
        for item, seller, amount in basket2_items:
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": buyer_tokens[1]},
                json={"item": item, "seller": seller, "amount": amount},
                exp_json={"message": "Item is added to the basket"},
                exp_code=201,
            )

        basket3_items = (("A1", sellers[0][0], 5), ("B3", sellers[1][0], 1))
        for item, seller, amount in basket3_items:
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": buyer_tokens[2]},
                json={"item": item, "seller": seller, "amount": amount},
                exp_json={"message": "Item is added to the basket"},
                exp_code=201,
            )

    with Scorer(2, "Amount of items to add to the basket must be positive"):
        for num in [-10, -5, -2, 0]:
            random_item = choice(["A1", "A2", "A3", "B1", "B2", "B3"])
            random_buyer_token = choice(buyer_tokens)
            random_seller = choice(sellers)
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": random_buyer_token},
                json={"item": random_item, "seller": random_seller[0], "amount": num},
                exp_json={"error": "Please specify a positive amount"},
                exp_code=400,
            )

    with Scorer(2, "Non-existent buyer can't add items to the basket"):
        for token in [*seller_tokens, "12345678"]:
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": token},
                json={"item": "A1", "seller": sellers[0], "amount": 5},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )

    with Scorer(4, "Can't pay if some item is unavailable due to insufficient stock"):
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[0]},
            exp_json={"error": "Insufficient stock"},
            exp_code=400,
        )

    with Scorer(2, "Buyer can remove specific item from a basket"):
        assert_response(
            c,
            "delete",
            "/buyer/item",
            headers={"token": buyer_tokens[0]},
            json={"item": "A1", "seller": sellers[0][0]},
            exp_json={"message": "Item is removed from the basket"},
            exp_code=200,
        )

    with Scorer(2, "Non-existent buyers can't remove items from basket"):
        for token in [*seller_tokens, "12345678"]:
            assert_response(
                c,
                "delete",
                "/buyer/item",
                json={"item": "A1", "seller": sellers[0][0]},
                headers={"token": token},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )

    with Scorer(4, "Can't pay if balance is insufficient"):
        assert_response(
            c,
            "post",
            "/buyer/item",
            headers={"token": buyer_tokens[0]},
            json={"item": "A1", "seller": sellers[0][0], "amount": 5},
            exp_json={"message": "Item is added to the basket"},
            exp_code=201,
        )
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[0]},
            exp_json={"error": "Please top up 260"},
            exp_code=400,
        )
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[1]},
            exp_json={"error": "Please top up 235"},
            exp_code=400,
        )

    with Scorer(2, "Successful top up"):
        assert_response(
            c,
            "post",
            "/buyer/topup",
            headers={"token": buyer_tokens[0]},
            json={"amount": 260},
            exp_json={"message": "Your balance is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "post",
            "/buyer/topup",
            headers={"token": buyer_tokens[1]},
            json={"amount": 300},
            exp_json={"message": "Your balance is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "post",
            "/buyer/topup",
            headers={"token": buyer_tokens[2]},
            json={"amount": 300},
            exp_json={"message": "Your balance is updated"},
            exp_code=200,
        )

    with Scorer(2, "Non-existent buyer can't top up"):
        for token in [*seller_tokens, "12345678"]:
            assert_response(
                c,
                "post",
                "/buyer/topup",
                headers={"token": token},
                json={"amount": 100},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )

    with Scorer(2, "Non-existent buyer can't make any payment"):
        for token in [*seller_tokens, "12345678"]:
            assert_response(
                c,
                "post",
                "/buyer/pay",
                headers={"token": token},
                exp_json={"error": "Unauthorized buyer"},
                exp_code=403,
            )

    with Scorer(2, "Succesful payment (ready stock + sufficient balance)"):
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[0]},
            exp_json={"message": "Payment is successsful"},
            exp_code=200,
        )
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[1]},
            exp_json={"message": "Payment is successsful"},
            exp_code=200,
        )

    with Scorer(2, "Succesful payment after stock is replenished"):
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[2]},
            exp_json={"error": "Insufficient stock"},
            exp_code=400,
        )
        assert_response(
            c,
            "put",
            "/seller/stock",
            json={"item": "A1", "amount": 5},
            headers={"token": seller_tokens[0]},
            exp_json={"message": "Item information is updated"},
            exp_code=200,
        )
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[2]},
            exp_json={"message": "Payment is successsful"},
            exp_code=200,
        )

    with Scorer(4, "Check revenue after purchases"):
        revenues = [310, 485]
        for index, revenue in enumerate(revenues):
            token = seller_tokens[index]
            assert_response(
                c,
                "get",
                "/seller/revenue",
                headers={"token": token},
                exp_json={"message": f"Your revenue is {revenue}"},
                exp_code=200,
            )

    with Scorer(
        2, "Check that basket is cleared after purchase and can't pay for empty basket"
    ):
        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[2]},
            exp_json={"error": "Basket is empty"},
            exp_code=400,
        )

    with Scorer(3, "Check buyer can re-purchase"):
        basket2_items = (
            ("A2", sellers[0][0], 2),
            ("A1", sellers[1][0], 2),
        )
        for item, seller, amount in basket2_items:
            assert_response(
                c,
                "post",
                "/buyer/item",
                headers={"token": buyer_tokens[1]},
                json={"item": item, "seller": seller, "amount": amount},
                exp_json={"message": "Item is added to the basket"},
                exp_code=201,
            )

        assert_response(
            c,
            "post",
            "/buyer/pay",
            headers={"token": buyer_tokens[1]},
            exp_json={"message": "Payment is successsful"},
            exp_code=200,
        )

    with Scorer(2, "Check final revenue"):
        revenues = [350, 509]
        for index, revenue in enumerate(revenues):
            token = seller_tokens[index]
            assert_response(
                c,
                "get",
                "/seller/revenue",
                headers={"token": token},
                exp_json={"message": f"Your revenue is {revenue}"},
                exp_code=200,
            )


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Project 2...")
    tests = [test_end_to_end]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Project 2:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
