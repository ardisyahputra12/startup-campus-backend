from antique import Antique
from market import Market
from seller import Seller
from basket import Basket


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
        self.name = name
        self.market = market
        self.basket = Basket()
        self.balance = 0
        self.registered = True
        self.market.add_buyer(self)
        # raise NotImplementedError("Please implement Buyer.__init__")

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
        if (self.name not in self.market.buyers) or self.registered == False:
            return "Buyer is not registered"
        if (self.name not in self.market.buyers) or seller.registered == False:
            return "Seller is not registered"
        if amount < 0 :
            return "Please specify a positive amount"
        self.basket.add_item(item, seller, amount)
        # raise NotImplementedError("Please implement Buyer.add_to_basket")

    # IMPLEMENT THIS
    def remove_from_basket(self, item: Antique, seller: Seller) -> str:
        """
        Remove ALL instances of an item sold by a given seller from the buyer's basket.
        For instance, if the basket contains 10 items of the same type, calling this
        function will remove all 10 from the basket.

        If the specified item doesn't exist in the basket, return "No such item in the basket".

        If all is good, alter the basket content accordingly and no need to return anything.
        """
        if self.name not in self.market.buyers or self.registered == False:
            return "Buyer is not registered"

        if not self.basket.remove_item(item, seller):
            return "No such item in the basket"
        # raise NotImplementedError("Please implement Buyer.remove_to_basket")

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
        if self.name not in self.market.buyers or self.registered == False:
            return "Buyer is not registered"

        if not self.basket.is_valid():
            return "Some items are out of stock"

        if any(self.basket.entries):

            total = self.basket.total_price(year_bought)
            if self.balance < total:
                return f"Insufficient balance, need to top up {total - self.balance}"

            self.balance -= total
            for i, j in self.basket.entries.items():
                for item_name, stock_exist in j.items():
                    i.sell_item(item_name, stock_exist, year_bought)
            self.basket.clear()
            return "All items are purchased!"
        else:
            return "No items to be paid"
        # raise NotImplementedError("Please implement Buyer.pay")

    # IMPLEMENT THIS
    def top_up(self, amount: int):
        """
        Top up the buyer's balance.

        When the buyer is first created, balance should be 0.
        """
        if self.name not in self.market.buyers or self.registered == False:
            return "Buyer is not registered"

        self.balance += amount
        # raise NotImplementedError("Please implement Buyer.top_up")
