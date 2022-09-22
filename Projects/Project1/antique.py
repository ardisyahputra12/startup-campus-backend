import uuid

class Antique:
    """
    Representation of an antique item.

    The selling price of an antique item is purely determined by:
        - year_created: the year the item is created
        - size: the size of the item

    For more details, please read explanation below on Coin/Stamp class.
    """

    # IMPLEMENT THIS
    def __init__(self, year_created: int, size: str):
        self.size = size
        self.year_created = year_created
        self.id = str(uuid.uuid4())
        # raise NotImplementedError("Please implement Antique.__init__")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


# IMPLEMENT THIS
class Coin(Antique):
    """
    Antique coin.

    The selling price follows this formula:
        BasePrice + (year_bought - year_created) * 1000

    BasePrice depends on the coin's size:
        - "small": 0
        - "medium": 25
    """
    def selling_price(self, year_bought):
        if self.size == "small":
            return 0 + (year_bought - self.year_created) * 1000
        if self.size == "medium":
            return 25 + (year_bought - self.year_created) * 1000


# IMPLEMENT THIS
class Stamp(Antique):
    """
    Antique stamp.

    The selling price follows this formula:
        BasePrice + (year_bought - year_created) * 500

    BasePrice depends on the stamp's size:
        - "small": 10
        - "medium": 50
        - "big": 250
    """
    def selling_price(self, year_bought):
        if self.size == "small":
            return 10 + (year_bought - self.year_created) * 500
        if self.size == "medium":
            return 50 + (year_bought - self.year_created) * 500
        if self.size == "big":
            return 250 + (year_bought - self.year_created) * 500
