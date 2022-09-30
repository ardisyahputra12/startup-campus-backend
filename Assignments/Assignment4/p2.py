"""
Candies and Chocolates.

In the beginning, you have 0 candies and chocolates. At any point, you want to be able to 
check your stock of candies and chocolates. And from time to time, you will be given
a random amount of candies and/or chocolates and add them to your current stock.

In this problem, you will implement endpoints that simulate those behaviors.

[CANDIES]

[[Endpoint]]
- Method: GET
- URL: /candies

[[Logic]]
- Check the number of candies you have at the moment, in the beginning you have 0.
    - return {"message": "I have <amount_of_candies> candies"}
        special case:
        - if <amount_of_candies> = 1, change the message to "I have 1 candy"
    - status code: 200


[CHOCOLATES]

[[Endpoint]]
- Method: GET
- URL: /chocolates

[[Logic]]
- Check the number of chocolates you have at the moment, in the beginning you have 0.
    - return {"message": "I have <amount_of_chocolates> chocolates"}
        special case:
        - if <amount_of_chocolates> = 1, change the mssage to "I have 1 chocolate"
    - status code: 200

[GIFT]

[[Endpoint]]
- Method: POST
- URL: /gifts
- Request body
    - candy: int (optional)
    - chocolate: int (optional)

[[Logic]]
0. If both "candy" and "chocolate" are not given in the request body:
    - return {"error": "No gifts for today :("}
    - status code; 400
1. gift is valid if it satisfies all of these:
    - either (number of) candy or chocolate is given in the request body (can be both)
    - all numbers must be positive
   on valid gifts:
    - update the stock of candy/chocolate respectively
    - return {"message": "Gifts are well received!"}
    - status code: 201
2. if the number of candy or chocolate is not a positive number:
    - return {"error": "We need real candies and chocolates"}
    - status code: 400
"""
from flask import Flask


def create_app():
    app = Flask(__name__)

    # IMPLEMENT THIS
    # Keep track the amount of candies and chocolates throughout
    # HINT: you can use:
    #   - Database (e.g. SQLite)
    #   - Use app.config[<key>] to store value and current_app.config[<key>] to retrieve
    return app


app = create_app()

# IMPLEMENT ALL ENDPOINTS below


# TEST IT YOURSELF
#   cd to Assignment4 folder
#   python3 p2.py
#
# please change the scenario as you wish
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    initial_candies_response = c.get("/candies")
    assert initial_candies_response.json == {"message": "I have 0 candies"}
    assert initial_candies_response.status_code == 200

    initial_chocs_response = c.get("/chocolates")
    assert initial_chocs_response.json == {"message": "I have 0 chocolates"}
    assert initial_chocs_response.status_code == 200

    gift_response = c.post("/gifts", json={"candy": 5, "chocolate": 3})
    assert gift_response.json == {"message": "Gifts are well received!"}
    assert gift_response.status_code == 201

    post_gift_candies_response = c.get("/candies")
    assert post_gift_candies_response.json == {"message": "I have 5 candies"}
    assert post_gift_candies_response.status_code == 200

    post_gift_chocolates_response = c.get("/chocolates")
    assert post_gift_chocolates_response.json == {"message": "I have 3 chocolates"}
    assert post_gift_chocolates_response.status_code == 200

    print("Testing p2.py DONE!")
