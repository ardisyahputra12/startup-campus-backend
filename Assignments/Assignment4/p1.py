"""
Rectangular area.

In this problem you need to develop an endpoint to find area of a rectangle. You will be given
the length and the width of the rectangle, and then return the area from the response.

[Endpoint]
- Method: GET 
- URL: /area
- Query parameters
    - length (integer)
    - width (integer)

[Logic]
1. If either length OR width is not positive, 
    - return {"error": "Both length and width must be positive numbers"}
    - status code: 400
2. If length is shorter than width
    - return {"error": "Length should not be shorter than width"}
    - status code: 400
3. If everything is valid:
    - return {"area": <rectangle_area>}
    - status code: 200

Keep in mind that formula for area of a rectangle is length * width.

Hint:
- You can access query parameters in a GET API via request.args, which will return a 
  dictionary (key-value, key = parameter, value = value of the parameter)

    from flask import request

    @app.route(...)
    def f():
        args = request.args 
        # args should be equal to dict-like object: {"k1": v1, "k2": v2, ...} 
        # you can access value of k1 as usual -> args["k1"] 
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/area", methods=["GET"])
def get_area():
    # IMPLEMENT THIS
    body = request.args
    length = body.get("length", type=int)
    width = body.get("width", type=int)

    if length < 1 or width < 1:
        return {
            "error": "Both length and with must be positive numbers"
        }, 400
    elif length < width:
        return {
            "error": "Length should not be shorter than width"
        }, 400
    else:
        return {
            "area": length * width
        }, 200


# TEST IT YOURSELF
#   cd to Assignment4 folder
#   python3 p1.py
#
# please change the scenario as you wish
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    valid_response = c.get("/area?length=5&width=3")
    assert valid_response.json == {"area": 15}
    assert valid_response.status_code == 200

    invalid_response1 = c.get("/area?length=-1&width=5")
    assert invalid_response1.json == {
        "error": "Both length and with must be positive numbers"
    }
    assert invalid_response1.status_code == 400

    invalid_response2 = c.get("/area?length=2&width=4")
    assert invalid_response2.json == {
        "error": "Length should not be shorter than width"
    }
    assert invalid_response2.status_code == 400

    print("Testing p1.py DONE!")
