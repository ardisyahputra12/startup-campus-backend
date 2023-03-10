from antique import Antique
from market import Market
from seller import Seller


class Buyer:
    """
    A person who can buy antique items on a given market.
    """

    # IMPLEMENT THIS
    def __init__(self, name: str, market: Market):
        """
        Each buyer is specified by a unique name on a given market.

        Each time a buyer is created successfully, the market should store his/her username.
        Can't register multiple buyers with the same name, only the first one is valid.

        A buyer B should be able to access his/her basket by calling B.basket

        In order to pay for something, buyer must have sufficient balance in the marketplace.
        Initially, the balance should be 0 but a buyer can top up any specific amount.
        """
        raise NotImplementedError("Please implement Buyer.__init__")

    # If you attempt to call any methods below with an unregistered buyer, return
    # "Buyer is not registered".

    # IMPLEMENT THIS
    def add_to_basket(self, item: Antique, seller: Seller, amount: int) -> str:
        """
        Add an item to this user's basket.

        Need to specify:
            - seller: from which seller the item will be bought
            - amount: the number of items of this type to be added

        Buyer can freely specify any amount even though the seller doesn't have enough stock
        at the moment. The stock will only be checked at the time of payment.

        If the amount isn't a positive integer, return "Please specify a positive amount"
        and do not alter the basket.

        If all is good, alter the basket content accordingly and no need to return anything.
        """
        raise NotImplementedError("Please implement Buyer.add_to_basket")

    # IMPLEMENT THIS
    def remove_from_basket(self, item: Antique, seller: Seller) -> str:
        """
        Remove ALL instances of an item sold by a given seller from the buyer's basket.
        For instance, if the basket contains 10 items of the same type, calling this
        function will remove all 10 from the basket.

        If the specified item doesn't exist in the basket, return "No such item in the basket".

        If all is good, alter the basket content accordingly and no need to return anything.
        """
        raise NotImplementedError("Please implement Buyer.remove_to_basket")

    # IMPLEMENT THIS
    def pay(self, year_bought: int) -> str:
        """
        Pay for ALL items in the user's basket on a specified year (year_bought).

        If the basket doesn't contain any items, return "No items to be paid".

        Then check whether corresponding sellers has sufficient stock for each item in the
        basket. If one of the item is out of stock, return "Some items are out of stock".

        If the buyer's balance is less than the total price of the items, return
            "Insufficient balance, need to top up X"
        where X is the difference betweenthe total price and the buyer's balance.

        If everything is good, do ALl of the following:
            - subtract the total price from the buyer's balance
            - remove each bought items from each seller's stock
            - clear the buyer's basket
            - return "All items are purchased!"
        """
        raise NotImplementedError("Please implement Buyer.pay")

    # IMPLEMENT THIS
    def top_up(self, amount: int):
        """
        Top up the buyer's balance.

        When the buyer is first created, balance should be 0.
        """
        raise NotImplementedError("Please implement Buyer.top_up")
