from flask import Flask, render_template, request, url_for, session
import json
from os.path import join, dirname, realpath

app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'

@app.route("/")
def start():
    session["user"] = False
    session["modo"] = False  # DEVENIR MODO ( ne peux pas se changer directement dans le site )
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/connection")
def connection():
    return render_template('connection.html')
    
@app.route("/connect", methods=['POST'])
def connect():
    session["nom"]=request.form["nom"]
    session["mdp"]=request.form["mdp"]
    print(session["nom"])
    print(session["mdp"])
    #########################################################
    if session["nom"] == "Alex" and session["mdp"] == 1:
    #########################################################
        session["user"] = True
        return render_template('index.html')
    else:
        return render_template('connection.html')

@app.route("/inscription")
def inscription():
    return render_template('inscription.html')

@app.route("/inscript", methods=['POST'])
def inscript():
    session["user"] = True
    return render_template('index.html')

@app.route("/profil")
def profil():
    return render_template('profil.html')

@app.route("/deconnexion")
def deconnexion():
    session["user"] = False
    return render_template('index.html')

@app.route("/presentation")
def presentation():
    return render_template('presentation.html')

@app.route("/moderation")
def moderation():
    return render_template('moderation.html')

@app.route("/jouer")
def jouer():
    return render_template('jouer.html')

@app.route("/course")
def course():
    return render_template('course.html')

@app.route("/combat")
def combat():
    return render_template('combat.html'""", ligne1, ligne2...""")

@app.route("/result_game")
def result_game():
    return render_template('result_game.html')

app.run(host = '127.0.0.1', port='5000', debug=True)