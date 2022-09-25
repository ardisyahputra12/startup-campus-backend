class Market:
    """
    A market is the place where people sell and buy antique items.

    Each new seller and buyer must register with unique username.

    Given a market M, we should be to access the following information:
        - M.buyers = list of usernames of all registered buyers, ordered alphabetically
        - M.sellers = list of usernames of all registered sellers, ordered alphabetically
    """

    # IMPLEMENT THIS
    def __init__(self, name: str):
        self.name = name
        self.buyers = []
        self.sellers = []
        # raise NotImplementedError("Please implement Market.__init__")

    ##########################################################################################
    # Helper Methods: you can implement any of these if you find them useful
    ##########################################################################################

    def insert_sorted(self, seq, elt):
        """inserts elt at the correct place in seq, to keep it in sorted order
        :param seq: A sorted list
        :param elt: An element comparable to the content of seq
        Effect: mutates the param seq.
        Does not return a result
        """
        idx = 0
        if not seq or elt > seq[-1]:
            seq.append(elt)
        else:
            while elt > seq[idx] and idx < len(seq):
                idx += 1
            seq.insert(idx, elt)

    def add_seller(self, seller):
        """Adds a new seller to this market and verify duplicate usernames."""
        if seller.name not in self.sellers:
            self.sellers.sort()
            self.insert_sorted(self.sellers, seller.name)
        else:
            seller.registered = False
            print(f"{seller.name} is already a registered seller")

    def add_buyer(self, buyer):
        """Adds a new buyer to this market and verify duplicate usernames."""
        if buyer.name not in self.buyers:
            self.buyers.sort()
            self.insert_sorted(self.buyers, buyer.name)
        else:
            buyer.registered = False
            print(f"{buyer.name} is already a registered buyer")
