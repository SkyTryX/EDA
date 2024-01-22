from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = b'6b1c2d979b55431bdc13c133bc026c80311b606aad7f3987b6638970bff1a5e1'

@app.errorhandler(404)
def notfound(error):
    return render_template("notfound.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/modmode")
def modmode():
    return render_template("modmode.html")

@app.route("/selector")
def selector():
    return render_template("selector.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")


app.run(host="127.0.0.1", port=8000, debug=True)