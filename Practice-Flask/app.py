from flask import Flask, request

app = Flask(__name__)

def do_the_login(nama):
    return nama

def show_the_login_form(nama):
    return f"DO GET {nama}"

@app.route("/", methods=['GET', 'POST'])
def login():
    # Untuk parameter
    nama = request.args.get("nama")
    if request.method == 'POST':
        return do_the_login(nama)
    else:
        return show_the_login_form(nama)

# put > replace data
# patch > modify data