"""
PLEASE DO NOT EDIT OR DELETE THIS FILE
"""
from functools import wraps
from io import StringIO
from unittest.mock import patch

from antique import Coin, Stamp
from buyer import Buyer
from market import Market
from seller import Seller

##############################################################################################
# Helpers
##############################################################################################


def grade(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
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


def assert_eq(expression, expected, exc_type=AssertionError):
    try:
        if expression == expected:
            return
        else:
            err = "\n".join([f"Expected: {expected}", f"Yours: {expression}"])
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


##############################################################################################
# Actual Tests
##############################################################################################


@grade
def test_single_marketplace():
    with Scorer(1, "Creating a marketplace"):
        my_shop = Market("Toko Antik")

    with Scorer(2, "Checking initial buyers/sellers"):
        assert_eq(my_shop.sellers, [])
        assert_eq(my_shop.buyers, [])

    # register 2 seller and 3 buyers (2 pts each for seller/buyer)
    with Scorer(1, "Registering valid sellers"):
        seller1 = Seller("Robert", my_shop)
        seller2 = Seller("Dwight", my_shop)
    with Scorer(1, "Registering valid buyers"):
        buyer1 = Buyer("Bob", my_shop)
        buyer2 = Buyer("Alice", my_shop)
        buyer3 = Buyer("Charlie", my_shop)

    # check printed statement when registering with existing username (2 pts each)
    with Scorer(1, "Registering illegal seller"):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            illegal_seller = Seller("Dwight", my_shop)
        assert_eq(
            mock_stdout.getvalue()[:-1],
            "Dwight is already a registered seller",
            exc_type=DisplayError,
        )
    with Scorer(1, "Registering illegal buyer"):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            illegal_buyer = Buyer("Charlie", my_shop)
        assert_eq(
            mock_stdout.getvalue()[:-1],
            "Charlie is already a registered buyer",
            exc_type=DisplayError,
        )

    # check list of sellers/buyers (2 pts each)
    with Scorer(2, "Checking registered sellers"):
        assert_eq(my_shop.sellers, ["Dwight", "Robert"])
    with Scorer(2, "Checking registered buyers"):
        assert_eq(my_shop.buyers, ["Alice", "Bob", "Charlie"])

    # check initial stuff
    with Scorer(2, "Checking initial revenues"):
        assert_eq(seller1.revenue, 0)
        assert_eq(seller2.revenue, 0)

    # stocking activities
    with Scorer(1, "Defining antique items"):
        # items to be stocked by Seller1
        item1_1 = Coin(1975, "small")
        item1_2 = Coin(1951, "small")
        item1_3 = Coin(1951, "medium")
        item1_4 = Stamp(1980, "small")
        item1_5 = Stamp(1950, "medium")
        item1_6 = Stamp(1970, "big")

        # items to be stocked by Seller2
        item2_1 = Coin(1975, "small")
        item2_2 = Coin(1951, "small")
        item2_3 = Coin(1900, "medium")
        item2_4 = Stamp(1930, "medium")
        item2_5 = Stamp(1920, "big")
        item2_6 = Stamp(1850, "big")

        # other items
        item3_1 = Coin(1976, "Small")
    with Scorer(5, "Seller should be able to stock antique items"):
        # seller1 stocks
        assert_eq(seller1.stock(item1_1, 5), "Stocking successful")
        assert_eq(seller1.stock(item1_2, 5), "Stocking successful")
        assert_eq(seller1.stock(item1_3, 2), "Stocking successful")
        assert_eq(seller1.stock(item1_4, 5), "Stocking successful")
        assert_eq(seller1.stock(item1_5, 3), "Stocking successful")
        assert_eq(seller1.stock(item1_6, 1), "Stocking successful")
        assert_eq(seller1.stock(item1_4, 5), "Stocking successful")
        # seller2 stocks
        assert_eq(seller2.stock(item2_1, 5), "Stocking successful")
        assert_eq(seller2.stock(item2_2, 3), "Stocking successful")
        assert_eq(seller2.stock(item2_3, 1), "Stocking successful")
        assert_eq(seller2.stock(item2_4, 5), "Stocking successful")
        assert_eq(seller2.stock(item2_1, 5), "Stocking successful")
        assert_eq(seller2.stock(item2_5, 1), "Stocking successful")
        assert_eq(seller2.stock(item2_6, 1), "Stocking successful")
    with Scorer(2, "Seller can only stock positive amount of items"):
        assert_eq(seller1.stock(item1_1, -3), "Please specify a positive amount")
        assert_eq(seller2.stock(item1_1, 0), "Please specify a positive amount")
    with Scorer(1, "Illegal seller shouldn't be able to stock"):
        assert_eq(illegal_seller.stock(item1_1, 100), "Seller is not registered")
        assert_eq(illegal_seller.stock(item3_1, -1), "Seller is not registered")
    with Scorer(1, "Revenue shouldn't change after stocking"):
        assert_eq(seller1.revenue, 0)
        assert_eq(seller2.revenue, 0)

    # adding items to basket
    with Scorer(2, "Buyer can add items to the basket"):
        # buyer1
        buyer1.add_to_basket(item1_1, seller1, 7)
        buyer1.add_to_basket(item1_2, seller1, 3)
        buyer1.add_to_basket(item1_4, seller1, 5)
        # buyer2
        buyer2.add_to_basket(item2_1, seller2, 5)
        buyer2.add_to_basket(item2_2, seller2, 3)
        buyer2.add_to_basket(item2_5, seller2, 1)
        # buyer3
        buyer3.add_to_basket(item1_1, seller1, 5)
        buyer3.add_to_basket(item1_4, seller1, 5)
        buyer3.add_to_basket(item2_5, seller2, 1)
    with Scorer(2, "Buyer can only stock positive amount of items"):
        buyer3.add_to_basket(item2_5, seller2, -1)
        buyer1.add_to_basket(item1_2, seller1, 0)
    with Scorer(1, "Illegal buyer shouldn't be able to modify basket"):
        assert_eq(
            illegal_buyer.add_to_basket(item1_1, seller1, 100),
            "Buyer is not registered",
        )
        assert_eq(
            illegal_buyer.add_to_basket(item3_1, seller1, -1), "Buyer is not registered"
        )
    with Scorer(1, "Buyer can't add item attached to illegal seller"):
        assert_eq(
            buyer1.add_to_basket(item1_1, illegal_seller, 100),
            "Seller is not registered",
        )
        assert_eq(
            buyer2.add_to_basket(item3_1, illegal_seller, -1),
            "Seller is not registered",
        )

    # remove from basket, and payment
    with Scorer(10, "Check out-of-stock items"):
        assert_eq(buyer1.pay(2020), "Some items are out of stock")
    with Scorer(2, "Check buyer can remove items from basket"):
        buyer1.remove_from_basket(item1_1, seller1)
        buyer1.add_to_basket(item2_1, seller2, 2)
    with Scorer(5, "Check buyer can't remove non-existent items from basket"):
        assert_eq(
            buyer1.remove_from_basket(item3_1, seller1), "No such item in the basket"
        )
        assert_eq(
            buyer1.remove_from_basket(item1_1, seller1), "No such item in the basket"
        )
    with Scorer(1, "Illegal buyer can't remove items from basket"):
        illegal_buyer.remove_from_basket(item1_1, seller1)
        illegal_buyer.remove_from_basket(item2_1, seller2)
    with Scorer(15, "Check for insufficient fund"):
        assert_eq(buyer1.pay(2020), "Insufficient balance, need to top up 397050")
    with Scorer(5, "Buyer should be able to top-up and pay for the whole basket"):
        buyer1.top_up(300000)
        assert_eq(buyer1.pay(2020), "Insufficient balance, need to top up 97050")
        buyer1.top_up(100000)
        assert_eq(buyer1.pay(2020), "All items are purchased!")
    with Scorer(1, "Illegal buyer can't top up"):
        assert_eq(illegal_buyer.top_up(2020), "Buyer is not registered")
    with Scorer(1, "Illegal buyer can't pay"):
        assert_eq(illegal_buyer.pay(2020), "Buyer is not registered")
    # cutoff: check revenue
    with Scorer(5, "Check revenue after 1st purchase"):
        assert_eq(seller1.revenue, 307050)
        assert_eq(seller2.revenue, 90000)

    with Scorer(7, "Check that item can be out of stock after being bought"):
        buyer2.top_up(500000)
        assert_eq(buyer2.pay(2020), "All items are purchased!")
        assert_eq(buyer3.pay(2020), "Some items are out of stock")
    with Scorer(2, "Check revenue after another purchase"):
        assert_eq(seller1.revenue, 307050)
        assert_eq(seller2.revenue, 572250)

    with Scorer(7, "Check buyer can buy item that got re-stocked"):
        assert_eq(seller2.stock(item2_5, 1), "Stocking successful")
        buyer3.top_up(383300)
        assert_eq(buyer3.pay(2021), "All items are purchased!")
        assert_eq(seller2.revenue, 623000)
        assert_eq(seller2.revenue, 623000)
        buyer2.add_to_basket(item2_5, seller2, 1)
        assert_eq(buyer2.pay(2021), "Some items are out of stock")

    with Scorer(
        3, "Basket should be cleared after purchase and can't pay for empty basket"
    ):
        assert_eq(buyer1.pay(2022), "No items to be paid")

    with Scorer(7, "Buyer can make another purchase"):
        buyer1.add_to_basket(item2_6, seller2, 1)
        buyer1.top_up(83300)
        assert_eq(buyer1.pay(2022), "All items are purchased!")
        assert_eq(seller1.stock(item1_5, 2), "Stocking successful")
        buyer2.remove_from_basket(item2_5, seller2)
        buyer2.add_to_basket(item1_5, seller1, 5)
        buyer2.top_up(162500)
        assert_eq(buyer2.pay(2022), "All items are purchased!")
        assert_eq(seller1.revenue, 819850)
        assert_eq(seller2.revenue, 709250)


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Grading Project 1...")
    tests = [test_single_marketplace]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}YOUR GRADE FOR Project 1:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
