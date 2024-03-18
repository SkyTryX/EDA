from flask import Flask, render_template, request, session, redirect
from os.path import join, dirname, realpath
import sqlite3
from functions.render import load_map_from_csv
from uuid import uuid4
from json import load, dump
from pathlib import Path
from functions.display_map import load_map
from random import randint
import json
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.route("/")
def start():
    session['uuid'] = None
    session['code'] = None
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
    if len(logging) != 0:
        session['uuid'] = cur.execute("SELECT uuid FROM donnee WHERE mail=?;",(request.form['mail'],)).fetchone()[0]
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
    con = sqlite3.connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    print(session['uuid'])
    pseudo = cur.execute("SELECT pseudo FROM donnee WHERE uuid=?;",(session['uuid'], )).fetchone()[0]
    mail = cur.execute("SELECT mail FROM donnee where uuid=?;",(session['uuid'], )).fetchone()[0]
    mail = f"*******{mail[3:]}"
    win = cur.execute("SELECT win FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0]
    elo = cur.execute("SELECT elo FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0]
    return render_template('profil.html', pseudo = pseudo, mail = mail, win = win, elo = elo)

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

@app.route("/queue", methods=['GET'])
def queue():
    """
    Système de queue indépendante du niveau, ajoute l'uuid du joueur qui cherche une partie dans 'gamemode' si aucune uuid n'est
    présente, si il y a une uuid ( et donc un joueur qui cherche ), lance un match avec 'other_player' avec l'uuid de l'autre joueur
    et remet la case 'gamemode' vide
    création de match : ajoute dans un json sous l'uuid 'matchuuid' le dictionnaire suivant :
    {"p1":session["uuid"],"p2":other_player,"map":"map","submission1":[], "submission2":[], "winner":None}
    """
    session["gamemode"] = request.args.get('gamemode')
    print(session['gamemode'])
    print(session['uuid'])
    if session["uuid"] != None:
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file_read:
            data = load(file_read)
            if data[session["gamemode"]] == "None":
                data[session["gamemode"]] = session["uuid"]
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    dump(data, file)
            elif data[session["gamemode"]][0] == session["uuid"][0]:
                return redirect("/")
            else:
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    other_player = data[session["gamemode"]]
                    data[session["gamemode"]] = "None"
                    matchuuid= str(uuid4())
                    session["match"] = matchuuid
                    with open(join(app.config['DATA_DIR'],f"matches/running/{matchuuid}.json"), "w") as file_match:
                        dump({"p1":session["uuid"],"p2":other_player,"map":"map","submission1":[], "submission2":[], "winner":None}, file_match)
                    data[session["gamemode"]] = "None"
                    dump(data, file)
    return render_template("queue.html")

@app.route("/combat", methods=['POST', 'GET'])
def combat():
    model = load_map(join(app.config['DATA_DIR'],f'maps/map{randint(1,1)}.csv'))
    SYMB = {
        'wall': ' X ',
        'free': '   ',
        'bot': [' @ ', ' # ']
    }
    w = model['w']
    h = model['h']
    mur = model['walls']
    bots = model['bot']

    truc = ""
    for x in range(w):
        for y in range(h):
            if (x, y) in mur:
                truc += SYMB['wall']
            else:
                is_bot = False
                for bot_id, bot_locations in bots.items():
                    if (x, y) in bot_locations:
                        truc += SYMB['bot'][int(bot_id) - 1]
                        is_bot = True
                if not is_bot:
                    truc += SYMB['free']
        truc += "\n"
    try:
        session['code'] =  request.form['code']
    except:
        IndexError
    if session['code'] != None:
            code_entrer = True
    else:
        code_entrer = False

    return render_template('combat.html', map=truc, gamemode=session['gamemode'],code=session['code'], code_entrer=code_entrer)

@app.route("/result_game")
def result_game():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    match = session["match"]
    with open(join(app.config['DATA_DIR'],f"matches/running/{match}.json"), "r") as file:
        data = json.load(file)
    with open(join(app.config['DATA_DIR'],f"matches/logs/{match}.json"), "w") as file_w:
        json.dump(data, file_w)
    Path.unlink(join(app.config['DATA_DIR'],f"matches/running/{match}.json"))
    if data["winner"] == session['uuid']:
        win = cur.execute("SELECT win FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET win=? WHERE uuid=? ;",( win, session['uuid'], )).fetchone()[0]
        victoire = True
    else:
        win = cur.execute("SELECT loss FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET loss=? WHERE uuid=? ;",( win, session['uuid'], )).fetchone()[0]
        victoire = False

    # Convert bot positions to tuples
    data["bots"]["bot1"] = tuple(data["bots"]["bot1"])
    data["bots"]["bot2"] = tuple(data["bots"]["bot2"])


    resultuuid= str(uuid4())
    with open(join(app.config['DATA_DIR'],f"matches/results/{resultuuid}.json"), "w") as file:
        json.dump(data, file)

    return render_template('result_game.html', victoire=victoire, carte=data['map'])

@app.route("/api/queue")
def return_queue():
    return load(open(join(app.config['DATA_DIR'],"matches/queue.json"), "r"))
"""
@app.route("/api/translator")
def return_translated():
    return eda_sharp(request.args.get("prog"))
"""

@socketio.on('send_maj')
def handle_send_maj(msg):
    emit('maj', {'data': 'New map data'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)