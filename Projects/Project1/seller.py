from antique import Antique
from market import Market

from basket import Basket


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
        self.basket = Basket()
        # raise NotImplementedError("Please implement Seller.__init__")

    def __str__(self) -> str:
        return self.market.add_seller(self.name)

    # IMPLEMENT THIS
    def stock(self, item: Antique, amount: int) -> str:
        """
        Stocks an antique item, and specify the amount as well.

        If this is an unregistered seller, return "Seller is not registered".

        If the amount isn't a positive integer, return "Please specify a positive amount"
        and do not alter the basket. Otherwise, the basket is valid and you need to alter
        the basket content accordingly and return "Stocking successful"
        """
        if (self.__str__() == f"{self.name} is already a registered seller"):
            if(amount <= 0):
                return "Please specify a positive amount"
            else:
                self.basket.is_valid(True)
        else:
            return "Seller is not registered"
        # raise NotImplementedError("Please implement Seller.stock")

    ##########################################################################################
    # Helper Methods: you can implement any of these if you find them useful
    ##########################################################################################

    def item_in_stock(self, item: Antique, amount: int) -> bool:
        """
        Checks whether an item is in seller's stock with at least the specified amount.

        Return True only if the seller's stock for this item >= amount.
        """
        pass

    def sell_item(self, item: Antique, amount: int, year_bought: int):
        """
        Sell and remove the given item (with the specified amount) from this seller's stock.

        Also modify revenue accordingly given the year the item is bought (year_bought).
        """
        pass
