from flask import Flask, render_template, request, session
from os.path import join, dirname, realpath
from random import *
import sqlite3
from render import load_map_from_csv

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
    return render_template('connection.html', erreur = False)
    
@app.route("/connect", methods=['POST'])
def connect():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'compte.db'))
    cur = con.cursor()
    try:
        mail = cur.execute("SELECT pseudo FROM donnee where mail=?;",(request.form['mail'], )).fetchone()[0]
        mdp = cur.execute("SELECT mdp FROM donnee where mail=?;",(request.form['mail'], )).fetchone()[0]
        if mail == request.form['mail'] and mdp  ==  request.form['mdp']:
            session['user'] = True
            return render_template("index.html")
        else:
            return render_template("connection.html", erreur = True)
    except : 
        TypeError
    return render_template("connection.html", erreur = True)

@app.route("/inscription")
def inscription():
    return render_template('inscription.html')

@app.route("/inscript", methods=['POST'])
def inscript():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'compte.db'))
    cur = con.cursor()
    mail = cur.execute("SELECT mail FROM donnee where pseudo=?;",(request.form['mail'], )).fetchone()
    pseudo = cur.execute("SELECT pseudo FROM donnee where pseudo=?;",(request.form['nom'], )).fetchone()
    if mail == None and pseudo == None:
        cur.execute("INSERT INTO donnee VALUES(?,?,?);",(request.form['mail'], request.form['nom'], request.form['mdp'],))
        cur.execute("INSERT INTO stat VALUES(?,?,?);",(request.form['nom'], 0, "plastique",))
        con.commit()
        session["user"] = True
        session['pseudo'] = request.form['nom']
        return render_template("index.html")
    else:   
        return render_template("inscription.html", erreur = True)

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
    map_data = load_map_from_csv('map.csv')
    return render_template('combat.html', map=map_data)

@app.route("/result_game")
def result_game():
    return render_template('result_game.html')

app.run(host = '127.0.0.1', port='5000', debug=True)