from flask import Flask, request

# buat endpoint yang return total angka dari 1 - N
#   method: GET
#   URL: /sum
#   query parameters:
#      - N: integer
# valid response:
# - return {"sum": <hasil>}
# - status code = 200
#
# if N < 1
# - return {"error": "N is smaller than 1"}
# - status code = 400

app = Flask(__name__)


@app.route("/sum", methods=["POST", "GET"])
def sum():
    args = request.args
    N = args.get("N")
    # print(N, type(N))
    # cast to desired type
    hasil = int(N)
    if hasil < 1:
        return {"error": "N is smaller than 1"}, 400
    else:
        total = 0
        # for jml in range(hasil):
        #     total = total + (jml + 1)
        for jml in range(1, hasil + 1):
            total += jml
        return {"sum": total}, 200


## TEST ##
if __name__ == "__main__":
    app.config.update({"TESTING": True})
    c = app.test_client()

    valid_response = c.post("/sum?N=3")
    print(valid_response.json)
    assert valid_response.json == {"sum": 6}
    assert valid_response.status_code == 200

    valid_response = c.post("/sum?N=100")
    assert valid_response.json == {"sum": 5050}
    assert valid_response.status_code == 200

    invalid_response = c.post("/sum?N=-1")
    assert invalid_response.json == {"error": "N is smaller than 1"}
    assert invalid_response.status_code == 400

    print("SUCCESS")
