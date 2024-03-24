from flask import Flask, render_template, request, session, redirect
from os.path import join, dirname, realpath
import sqlite3
from uuid import uuid4
from json import load, dump
from pathlib import Path
from functions.display_map import load_map, SYMB
from random import randint
from flask_socketio import SocketIO, emit
from functions.eda_sharp.eda_python import *



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

@app.route("/inscript", methods=['POST', 'GET'])
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
    session["bot"] = None
    if session.get("uuid") != None:
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file_read:
            data = load(file_read)
            if data[request.args.get('gamemode')] == "None":
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    matchuuid= str(uuid4())
                    data[request.args.get('gamemode')] = [session["uuid"], matchuuid]
                    dump(data, file)
                session["bot"] = "1"
                session["match"] = matchuuid

            elif data[request.args.get('gamemode')][0] == session["uuid"][0]:
                return redirect("/")
            
            else:
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    other_player = data[request.args.get('gamemode')][0]
                    session["match"] = data[request.args.get('gamemode')][1]
                    data[request.args.get('gamemode')] = "None"
                   
                    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as file_match:
                        dump({"p1":session["uuid"],"p2":other_player, "pos_p1": [0, 0], "pos_p2": [10, 14], "shields":[] ,"map":"map", "winner":None}, file_match)
                    data[request.args.get('gamemode')] = "None"
                    dump(data, file)
                    session["bot"] = "2"
    else:
        return redirect("/")
    return render_template("queue.html")

@app.route("/combat", methods=['POST', 'GET'])
def combat():
    model = load_map(join(app.config['DATA_DIR'],f'maps/map{randint(1,1)}.csv'))
    cmds = None
    if request.form.get('code') != None:
        cmds = compileur(lexxer(request.form['code']))
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
            data = load(match_file)
        if data["pos_p"+session["bot"]] == None:
            data["pos_p"+session["bot"]] = model["bot"][session["bot"]]
        memory[pos_x] = data["pos_p"+session["bot"]][0]
        memory[pos_y] = data["pos_p"+session["bot"]][1]
        for code in cmds:
            if len(code[1]) != 0:
                code[0](code[1][0])
            else:
                code[0](model["walls"])
        data["pos_p"+session["bot"]] = [memory[pos_x], memory[pos_y]]
        model["bot"][session["bot"]] = [memory[pos_y], memory[pos_x]]
        ennemy = '1' if session['bot'] == '2' else '2'
        model["bot"][ennemy] = [data["pos_p"+ennemy][1], data["pos_p"+ennemy][0]]
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as match_file:
            dump(data, match_file)        

    map_str = ""
    for x in range(model['w']):
        for y in range(model['h']):
            has_shield = False
            for s in memory[shields]:
                if (x, y) == list(s.keys())[0]:
                    has_shield = True
            if [x, y] in model['walls']:
                if has_shield:
                    map_str += SYMB['shield'][0]
                else:
                    map_str += SYMB['wall']
            elif [x, y] == model["bot"]["1"]:
                map_str += SYMB['bot'][0]
            elif [x, y] == model["bot"]["2"]:
                map_str += SYMB['bot'][1]
            else:
                if has_shield:
                    map_str += SYMB['shield'][1]
                else:
                    map_str += SYMB['free']
        map_str += "\n"
    return render_template('combat.html', map=map_str, code_entrer=(cmds != None), bot=session["bot"])

@app.route("/result_game")
def result_game():
    con = sqlite3.connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    match = session["match"]
    with open(join(app.config['DATA_DIR'],f"matches/running/{match}.json"), "r") as file:
        data = load(file)
    with open(join(app.config['DATA_DIR'],f"matches/logs/{match}.json"), "w") as file_w:
        dump(data, file_w)
    Path.unlink(join(app.config['DATA_DIR'],f"matches/running/{match}.json"))
    if data["winner"] == session['uuid']:
        win = cur.execute("SELECT win FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET win=? WHERE uuid=? ;",( win, session['uuid'], )).fetchone()[0]
        victoire = True
    else:
        win = cur.execute("SELECT loss FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET loss=? WHERE uuid=? ;",( win, session['uuid'], )).fetchone()[0]
        victoire = False

    data["bots"]["bot1"] = tuple(data["bots"]["bot1"])
    data["bots"]["bot2"] = tuple(data["bots"]["bot2"])


    resultuuid= str(uuid4())
    with open(join(app.config['DATA_DIR'],f"matches/results/{resultuuid}.json"), "w") as file:
        dump(data, file)

    return render_template('result_game.html', victoire=victoire, carte=data['map'])

@app.route("/api/queue")
def return_queue():
    return load(open(join(app.config['DATA_DIR'],"matches/queue.json"), "r"))


@socketio.on('send_maj')
def handle_send_maj(msg):
    emit('send_maj', {'data': 'New map data'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)