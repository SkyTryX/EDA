from flask import Flask, render_template, request, session, redirect
from os.path import join, dirname, realpath
import sqlite3
from functions.render import load_map_from_csv
from functions.parser import eda_sharp
from uuid import uuid4
from json import load, dump
from pathlib import Path
from display import display

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
        uuid = str(uuid4())
        cur.execute("INSERT INTO donnee VALUES(?,?,?,?);",(uuid, request.form['mail'], request.form['nom'], request.form['mdp']))
        cur.execute("INSERT INTO stats VALUES(?,?,?);",(uuid, 0, 1400,))
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

@app.route("/queue")
def queue():
    session["gamemode"] = "course"
    if session["uuid"] != None:
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file_read:
            data = load(file_read)
            print(data[session["gamemode"]][0], session["uuid"][0])
            if data[session["gamemode"]] == "None":
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    data[session["gamemode"]] = session["uuid"]
                    dump(data, file)
            elif data[session["gamemode"]][0] == session["uuid"][0]:
                return redirect("/")
            else:
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    other_player = data[session["gamemode"]]
                    data[session["gamemode"]] = "None"
                    dump(data, file)
                matchuuid= str(uuid4())
                with open(join(app.config['DATA_DIR'],f"matches/running/{matchuuid}.json"), "w") as file:
                    session["match"] = matchuuid
                    dump({"p1":session["uuid"],"p2":other_player,"map":"map","submission1":[], "submission2":[], "winner":None}, file)
    return render_template("queue.html")

@app.route("/course")
def course():
    map_data = load_map_from_csv(join(app.config['DATA_DIR'],'maps/map.csv'))
    return render_template('course.html', map=map_data)

@app.route("/combat")
def combat():
    map_ascii = display()
    return render_template('combat.html', map=map_ascii)

@app.route("/result_game")
def result_game():
    match = session["match"]
    with open(join(app.config['DATA_DIR'],f"matches/running/{match}.json"), "w") as file:
        data = load(file)
        with open(join(app.config['DATA_DIR'],f"matches/logs/{match}.json"), "w") as file_w:
            dump(data, file_w)
    Path.unlink(join(app.config['DATA_DIR'],f"matches/running/{match}.json"))
    return render_template('result_game.html')

@app.route("/api/queue")
def return_queue():
    return load(open(join(app.config['DATA_DIR'],"matches/queue.json"), "r"))

@app.route("/api/translator")
def return_translated():
    return eda_sharp(request.args.get("prog"))


app.run(host = '127.0.0.1', port='5000', debug=True)