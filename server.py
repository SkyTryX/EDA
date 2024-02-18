from flask import Flask, render_template, request, session
from os.path import join, dirname, realpath
import sqlite3
from functions.render import load_map_from_csv
from uuid import uuid4

app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'

@app.route("/")
def start():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/connection")
def connection():
    return render_template('connection.html', erreur=False)
    
@app.route("/connect", methods=['POST'])
def connect():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    logging = cur.execute("SELECT mail, mdp FROM donnee WHERE mail=? AND mdp=?;",(request.form['mail'], request.form['mdp'])).fetchall()
    if logging != None:
        session['uuid'] = cur.execute("SELECT uuid FROM donnee WHERE mail=?;",(request.form['mail'],)).fetchone()
        return render_template("index.html")
    else:
        return render_template("connection.html", erreur = True)

@app.route("/inscription")
def inscription():
    return render_template('inscription.html')

@app.route("/inscript", methods=['POST'])
def inscript():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    mail = cur.execute("SELECT mail FROM donnee where pseudo=?;",(request.form['mail'], )).fetchone()
    pseudo = cur.execute("SELECT pseudo FROM donnee where pseudo=?;",(request.form['nom'], )).fetchone()
    if mail == None and pseudo == None:
        uuid = uuid4()
        cur.execute("INSERT INTO donnee VALUES(?,?,?,?);",(str(uuid), request.form['mail'], request.form['nom'], request.form['mdp']))
        cur.execute("INSERT INTO stats VALUES(?,?,?);",(str(uuid), 0, 1400,))
        con.commit()
        session['uuid'] = uuid
        return render_template("index.html")
    else:   
        return render_template("inscription.html", erreur = True)

@app.route("/profil")
def profil():
    return render_template('profil.html')

@app.route("/deconnexion")
def deconnexion():
    session["uuid"] = None
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
    map_data = load_map_from_csv(join(app.config['DATA_DIR'], '/maps/map.csv'))
    return render_template('combat.html', map=map_data)

@app.route("/result_game")
def result_game():
    return render_template('result_game.html')

app.run(host = '127.0.0.1', port='5000', debug=True)