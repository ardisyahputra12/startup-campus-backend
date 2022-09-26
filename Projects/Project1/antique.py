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
        raise NotImplementedError("Please implement Antique.__init__")


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
