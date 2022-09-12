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
        raise NotImplementedError("Please implement Market.__init__")

    ##########################################################################################
    # Helper Methods: you can implement any of these if you find them useful
    ##########################################################################################

    def add_seller(self, seller):
        """Adds a new seller to this market and verify duplicate usernames."""
        pass

    def add_buyer(self, buyer):
        """Adds a new buyer to this market and verify duplicate usernames."""
        pass
