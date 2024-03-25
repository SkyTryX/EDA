from flask import Flask, render_template, request, session, redirect, jsonify
from os.path import join, dirname, realpath
import sqlite3
from uuid import uuid4
from json import load, dump
from pathlib import Path
from functions.display_map import load_map, SYMB
from random import randint
from flask_socketio import SocketIO
from functions.eda import *
from functions.verifie_code import *


app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.route("/")
def start():
    session['uuid'] = None
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
    session["bot"] = None
    if session.get("uuid") != None: # SI LE JOUEUR EXISTE
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file_read:
            data = load(file_read)
            if data[request.args.get('gamemode')] == "None": # SI PERSONNE NE QUEUE
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    matchuuid= str(uuid4())
                    data[request.args.get('gamemode')] = [session["uuid"], matchuuid]
                    dump(data, file)
                session["bot"] = "1"
                session["match"] = matchuuid

            elif data[request.args.get('gamemode')][0] == session["uuid"][0]: # SI UNE MEME PERSONNE QUEUE 2 FOIS
                return redirect("/")
            
            else: # SI LE JOUEUR QUEUE DANS UNE QUEUE DEJA PLEINE
                with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
                    other_player = data[request.args.get('gamemode')][0]
                    session["match"] = data[request.args.get('gamemode')][1]
                    data[request.args.get('gamemode')] = "None"
                   
                    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as file_match:
                        dump({"p1":session["uuid"],"p2":other_player, "pos_p1": [0, 0], "pos_p2": [10, 15], "shields":[] ,"map":"map", "winner":None}, file_match)
                    data[request.args.get('gamemode')] = "None"
                    dump(data, file)
                    session["bot"] = "2"
                    return redirect("/combat")
    else:
        return redirect("/")
    return render_template("queue.html", gamemode=request.args.get("gamemode"))

@app.route("/combat", methods=['POST', 'GET'])
def combat():
    model = load_map(join(app.config['DATA_DIR'],f'maps/map{randint(1,1)}.csv'))
    cmds = None
    if request.form.get('code') != None: # SI UN CODE A ETE ENVOYE
        cmds = compileur(lexxer(request.form['code']))
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
            data = load(match_file) # ON PREND LES INFOS SUR LE MATCH

        # ON INITIALISE LA POSITION DU BOT POUR L'INTERPRETEUR
        memory[pos_x] = data["pos_p"+session["bot"]][0]
        memory[pos_y] = data["pos_p"+session["bot"]][1]

        # CHECK POUR VOIR SI LE JOUEUR EST EN SHIELD
        in_shield = False
        for s in data["shields"]:
            if s["bot"] == session["bot"]:
                in_shield = True
                break

        # SI IL N'EST PAS EN SHIELD
        if not in_shield:
            # EXECUTION DU CODE
            for code in cmds:
                if len(code[1]) != 0:
                    code[0](code[1][0])
                else:
                    code[0](model["walls"])
                if code[0].__name__ == "shield":
                    break # ARRET D'EXECUTION SI ON A SHIELD (A CHANGER PROB)

        data["pos_p"+session["bot"]] = [memory[pos_x], memory[pos_y]]
        model["bot"][session["bot"]] = [memory[pos_y], memory[pos_x]]
        ennemy = '1' if session['bot'] == '2' else '2'
        model["bot"][ennemy] = [data["pos_p"+ennemy][1], data["pos_p"+ennemy][0]]

        #CHECK POUR VOIR SI UN SHIELD A EXPIRE
        pop_indexes = []
        for i in range(len(data["shields"])):
            if data["shields"][i]["bot"] == session["bot"]:
                data["shields"][i]["tour"] -= 1
            if data["shields"][i]["tour"] == 0:
                pop_indexes.append(i)
        pop_indexes.reverse()
        for index in pop_indexes:
            data["shields"].pop(index)
        for s in memory[shields]:
            data["shields"].append({"coords":s[0],"tour":int(s[1]),"bot":session["bot"]})
        memory[shields] = []

        # ON ACTUALISE LE JSON AVEC TOUT LES CHANGEMENTS
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as match_file:
            dump(data, match_file)
    
    # CREATION DE LA MAP
    map_str = ""
    for x in range(model['w']):
        for y in range(model['h']):
            has_shield = False
            for s in data["shields"]:
                if [x, y] == s["coords"]:
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

    # DEPLACEMENT DU FICHIER JSON
    with open(join(app.config['DATA_DIR'],f"matches/running/{match}.json"), "r") as file:
        data = load(file)
    with open(join(app.config['DATA_DIR'],f"matches/logs/{match}.json"), "w") as file_w:
        dump(data, file_w)
    Path.unlink(join(app.config['DATA_DIR'],f"matches/running/{match}.json"))

    # AJOUT DES STATISTIQUES (+1 VICTOIRE)
    if data["winner"] == session['uuid']:
        win = cur.execute("SELECT win FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET win=? WHERE uuid=?;",( win, session['uuid'], )).fetchone()[0]
        victoire = True
    else:
        win = cur.execute("SELECT loss FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0] + 1
        cur.execute("UPDATE stats SET loss=? WHERE uuid=?;",( win, session['uuid'], )).fetchone()[0]
        victoire = False
    con.commit()
    return render_template('result_game.html', victoire=victoire)

@app.route("/api/queue")
def return_queue():
    return load(open(join(app.config['DATA_DIR'],"matches/queue.json"), "r"))

@app.route('/verify', methods=['POST'])
def verify_code():
    resultat = eda_linter(spliter(request.json['code']))
    return jsonify({'result': resultat[0], 'error': resultat[1]})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)