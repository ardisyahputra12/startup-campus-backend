from collections import defaultdict

class Basket:
    """
    A basket is a collection of antique items to be bought. Each basket is tied to
    a specific buyer B and the basket should be accessible by calling B.basket

    Each item in the basket is sold by a unique seller.
    """

    def __init__(self):
        # store basket entries with a dictionary, feel free to change if you can find
        # and implement better alternatives
        self.entries = defaultdict(dict)
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
        if seller not in self.entries:
            self.entries[seller] = {}
            self.entries[seller][item] = 0
        elif item not in self.entries[seller]:
            self.entries[seller][item] = 0
        self.entries[seller][item] += amount

    def remove_item(self, item, seller) -> str:
        """Removes all occurences of an item sold by a seller from this basket"""
        if item not in self.entries[seller]:
            return False
        else:
            del self.entries[seller][item]
            return True

    def is_valid(self) -> bool:
        """Return True if each item in the basket is in-stock."""
        for seller, items in self.entries.items():
            for item, amount in items.items():
                if not seller.item_in_stock(item, amount):
                    return False
        return True

    def total_price(self, year_bought: int) -> int:
        """Return total price of all items in the basket if bought on the specified year."""
        total = 0
        for seller,items in self.entries.items():
            for item,amount in items.items():
                total += item.selling_price(year_bought) * amount
        return total

    def clear(self):
        """
        Remove all items already stored in this basket.
        """
        self.entries = {}
