from antique import Antique
from market import Market
from collections import defaultdict

class Seller:
    """
    A person who can sell antique items on a given market.

    Each time a seller is created successfully, the market should store his/her username.
    Can't register multiple sellers with the same name, only the first one is valid.

    A seller S should be able to get the total revenue from selling the items at any given
    time by calling S.revenue
    """

    # IMPLEMENT THIS
    def __init__(self, name: str, market: Market):
        """
        Each seller is specified by a unique name on a given market.
        """
        self.name = name
        self.market = market
        self.stocks = defaultdict(dict)
        self.revenue = 0
        self.registered = True
        self.market.add_seller(self)
        # raise NotImplementedError("Please implement Seller.__init__")

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.name, self.registered) == (other.name, other.registered)

    # IMPLEMENT THIS
    def stock(self, item: Antique, amount: int) -> str:
        """
        Stocks an antique item, and specify the amount as well.

        If this is an unregistered seller, return "Seller is not registered".

        If the amount isn't a positive integer, return "Please specify a positive amount"
        and do not alter the basket. Otherwise, the basket is valid and you need to alter
        the basket content accordingly and return "Stocking successful"
        """
        if (self.name not in self.market.sellers) or self.registered == False:
            return "Seller is not registered"

        if amount <= 0: return "Please specify a positive amount"

        if item in self.stocks: self.stocks[item] += amount
        else: self.stocks[item] = amount

        return "Stocking successful"
        # raise NotImplementedError("Please implement Seller.stock")

    ##########################################################################################
    # Helper Methods: you can implement any of these if you find them useful
    ##########################################################################################

    def item_in_stock(self, item: Antique, amount: int) -> bool:
        """
        Checks whether an item is in seller's stock with at least the specified amount.

        Return True only if the seller's stock for this item >= amount.
        """
        if self.name not in self.market.sellers or self.registered == False:
            return "Seller is not registered"
        if item not in self.stocks: return False
        if self.stocks[item] >= amount: return True

        return False

    def sell_item(self, item: Antique, amount: int, year_bought: int):
        """
        Sell and remove the given item (with the specified amount) from this seller's stock.

        Also modify revenue accordingly given the year the item is bought (year_bought).
        """
        if (self.name not in self.market.sellers) or self.registered == False:
            return "Seller is not registered"

        if self.stocks[item] > amount: self.stocks[item] -= amount
        else: del self.stocks[item]

        self.revenue += item.selling_price(year_bought) * amount
