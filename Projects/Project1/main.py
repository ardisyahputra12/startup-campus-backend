"""
Antique marketplace.

In this project, you are given a simple simulation of marketplace of antique items. 
You need to implement the behavior of the following objects:
    - Market: a marketplace where people can buy and sell antique items
    - Seller: a seller in a given market
    - Buyer: a buyer in a given market
    - Antique: antique item that can be sold and bought in the market
    - Basket: a list of items gathered by the buyer, before being paid and bought

Please check the following files for more detailed explanations:
    - Market -> market.py
    - Seller -> seller.py
    - Buyer -> buyer.py
    - Basket -> basket.py
    - Antique items -> antique.py

TO DO:
    - Implement ALL the functions and classes with IMPLEMENT THIS signs on those files
    - You may optionally implement additional functions or classes as you see fit
    - Feel free to discuss the high-level ideas with your friend (but not the code)

DO NOT:
    - Remove any functions/methods/classes given to you
    - Import additional library outside of the standard Python library
    - Copy paste exact implementation from anyone
"""

from antique import Coin, Stamp
from buyer import Buyer
from market import Market
from seller import Seller

# You can test these sequence of logics by following these steps:
#   - cd to Project1 folder
#   - python3 main.py


def assert_eq(expression, expected):
    try:
        if expression == expected:
            return
    except Exception as e:
        raise Exception(f"Expression can't be evaluated: {e}")

    raise Exception(f"Expected: {expected}, your value: {expression}")


#############################################################################
# Marketplace initiation
#############################################################################
# create new marketplace
my_shop = Market("Toko Antik")

# register 1 seller and 2 buyers
seller1 = Seller("S1", my_shop)
buyer1 = Buyer("B1", my_shop)
buyer2 = Buyer("B2", my_shop)

# can't register with the same username
invalid_seller = Seller("S1", my_shop)
#   should print "S1 is already a registered seller"
invalid_buyer = Buyer("B2", my_shop)
#   should print "B2 is already a registered buyer"

# check the list of sellers and buyers
assert_eq(my_shop.sellers, ["S1"])
assert_eq(my_shop.buyers, ["B1", "B2"])

#############################################################################
# Seller stocks things to sell
#############################################################################
# stock 2x small coin created on year 1950
item1 = Coin(1950, "small")
assert_eq(seller1.stock(item1, 2), "Stocking successful")

# stock another small coin created on year 1950, but this is considered a different item
item2 = Coin(1950, "small")
assert_eq(seller1.stock(item2, 1), "Stocking successful")

# stock 2x medium coin created on year 1970
item3 = Coin(1970, "medium")
assert_eq(seller1.stock(item3, 2), "Stocking successful")


# stock 1x big stamp created on year 1900
item4 = Stamp(1900, "big")
assert_eq(seller1.stock(item4, 1), "Stocking successful")
assert_eq(seller1.stock(item3, -3), "Please specify a positive amount")

# check that seller has 0 revenue in the beginning
assert_eq(seller1.revenue, 0)

# invalid seller can't stock things
assert_eq(invalid_seller.stock(item2, 100), "Seller is not registered")

# At this point, seller1 should have stocked the following items:
#   - Item1: 2x small coins (1950)
#   - Item2: 1x small coin (1950)
#   - Item3: 2x medium coins (1970)
#   - Item4: 1x big stamp (1900)

#############################################################################
# Buyers attempt to add/remove things in their basket
#############################################################################
# buyer 1's activities
buyer1.add_to_basket(item1, seller1, 2)
buyer1.add_to_basket(item4, seller1, 1)
assert_eq(buyer1.add_to_basket(item3, seller1, -1), "Please specify a positive amount")

# buyer2's activities
buyer2.add_to_basket(item2, seller1, 2)
buyer2.add_to_basket(item3, seller1, 3)
# will remove all item3 in the basket
buyer2.remove_from_basket(item3, seller1)

# attempt to add an item NOT owned by the seller, should be fine for now
item5 = Stamp(1972, "small")
buyer2.add_to_basket(item5, seller1, 3)
# let's call this Item5: 1x small stamp (1972)

# invalid buyer can't add items
assert_eq(invalid_buyer.add_to_basket(item1, seller1, 2), "Buyer is not registered")

# At this point, the baskets should look as follows:
#
# [buyer1's basket]
#   - 2x Item1
#   - 1x Item4
#
# [buyer2's basket]
#   - 2x Item2
#   - 3x Item5

#############################################################################
# Buyers attempt to pay for the items
#############################################################################

# Before continuing, please read antique.py for the pricing rule for Coin and Stamp.
#
# Let's take a look at the price for each item in buyer1's basket (in the year 2022):
# - Item1: 0 + (2022 - 1950) * 1000 = 72000
# - Item4: 250 + (2022 - 1900) * 500 = 61250
#
# Total price: 2*Item1 + Item4 = 20520

# should fail due to insufficient balance
assert_eq(buyer1.pay(year_bought=2022), "Insufficient balance, need to top up 205250")

# topping up 200k is not enough
buyer1.top_up(200000)
assert_eq(buyer1.pay(year_bought=2022), "Insufficient balance, need to top up 5250")

# topping up another 10k
buyer1.top_up(10000)
assert_eq(buyer1.pay(year_bought=2022), "All items are purchased!")

# At this point, this is the status of seller1's stock:
#   - Item2: 1x small coin (1950)
#   - Item3: 2x medium coins (1970)

# since the basket is cleared after the purchase, it is empty now
assert_eq(buyer1.pay(year_bought=2023), "No items to be paid")

# should fail as Item5 is not in the seller1's stock
assert_eq(buyer2.pay(year_bought=2022), "Some items are out of stock")

# remove Item5 from the basket
buyer2.remove_from_basket(item5, seller1)
# buyer2's basket will look like this now:
#   - 2x Item2

# re-attemps to buy, but still fail since seller1 has only 1x Item2
assert_eq(buyer2.pay(year_bought=2022), "Some items are out of stock")

# seller1 stocks 1 more Item2
assert_eq(seller1.stock(item2, 1), "Stocking successful")
# then buyer2 re-attempts to buy in the following year
# now the stock issue is resolved, but buyer2 doesn't have sufficient balance
assert_eq(buyer2.pay(year_bought=2023), "Insufficient balance, need to top up 146000")

# top up exact amount, then pay
buyer2.top_up(146000)
assert_eq(buyer2.pay(year_bought=2023), "All items are purchased!")

# at this point, seller1 has obtained the following revenue from each buyer:
#   - buyer1: 205250
#   - buyer2: 146000
# giving a total of 351250
assert_eq(seller1.revenue, 351250)

# invalid buyer can't top up
assert_eq(invalid_buyer.top_up(1000000000), "Buyer is not registered")

print("Congratulations, you pass the basic case! Now let's try to pass the grader.")
