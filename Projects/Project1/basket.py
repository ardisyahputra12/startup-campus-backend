class Basket:
    """
    A basket is a collection of antique items to be bought. Each basket is tied to
    a specific buyer B and the basket should be accessible by calling B.basket

    Each item in the basket is sold by a unique seller.
    """

    def __init__(self):
        # store basket entries with a dictionary, feel free to change if you can find
        # and implement better alternatives
        self.entries = {}
        # HINT: try storing the items with the following hierarchy:
        # - seller
        # - item
        # - item occurence (amount)
        #
        # the structure will be as follows:
        # self.entries = {
        #   <seller1>: {
        #       <item_id1>: amount1,
        #       <item_id2>: amount2
        #   },
        #   <seller2>: {...},
        #   ...
        # }

    ##########################################################################################
    # Helper Methods: you can implement any of these if you find them useful
    ##########################################################################################

    def add_item(self, item, seller, amount) -> str:
        """Adds an item sold by a seller to this basket, with the specified amount."""
        pass

    def remove_item(self, item, seller) -> str:
        """Removes all occurences of an item sold by a seller from this basket"""
        pass

    def is_valid(self) -> bool:
        """Return True if each item in the basket is in-stock."""
        pass

    def total_price(self, year_bought: int) -> int:
        """Return total price of all items in the basket if bought on the specified year."""
        pass

    def clear(self):
        """
        Remove all items already stored in this basket.
        """
        self.entries = {}
