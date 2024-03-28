from flask import Flask, render_template, request, session, redirect, jsonify
from os.path import join, dirname, realpath
from sqlite3 import connect
from uuid import uuid4
from json import load, dump, decoder
from pathlib import Path
from functions.display_map import load_map, SYMB
from random import randint
from functions.eda_sharp import spliter, lexxer, EdaExecutor, pos_x, pos_y, shields, compileur
from functions.verifie_code import eda_linter
from functions.mailcheck import is_valid_mail
from time import sleep

app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'

@app.errorhandler(404)
def notfound(e):
    return render_template("notfound.html")

@app.route("/")
def index():
    return render_template('index.html', not_connected=session.get("uuid")== None)

@app.route("/connection")
def connection():
    return render_template('connection.html', erreur=False)

@app.route("/deconnexion")
def deconnection():
    session["uuid"] = None
    return redirect("/")
    
@app.route("/connect", methods=['POST'])
def connection_error():
    con = connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    logging = cur.execute("SELECT mail, mdp FROM donnee WHERE mail=? AND mdp=?;",(request.form['mail'], request.form['mdp'])).fetchall()
    if len(logging) != 0:
        session['uuid'] = cur.execute("SELECT uuid FROM donnee WHERE mail=?;",(request.form['mail'],)).fetchone()[0]
        return redirect("/")
    else:
        return render_template("connection.html", erreur = True)


@app.route("/inscription")
def inscription():
    return render_template('inscription.html')

@app.route("/inscript", methods=['POST', 'GET'])
def inscript():
    con = connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    mail = cur.execute("SELECT mail FROM donnee where pseudo=?;",(request.form['mail'], )).fetchone()
    pseudo = cur.execute("SELECT pseudo FROM donnee where pseudo=?;",(request.form['nom'], )).fetchone()
    if (mail == None and pseudo == None) and not (len(request.form['nom']) <= 2 or not is_valid_mail(request.form['mail'])):
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
    con = connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    pseudo = cur.execute("SELECT pseudo FROM donnee WHERE uuid=?;",(session['uuid'], )).fetchone()[0]
    mail = cur.execute("SELECT mail FROM donnee where uuid=?;",(session['uuid'], )).fetchone()[0]
    mail = f"*******{mail[3:]}"
    win = cur.execute("SELECT win FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0]
    elo = cur.execute("SELECT elo FROM stats where uuid=?;",(session['uuid'], )).fetchone()[0]
    return render_template('profil.html', pseudo = pseudo, mail = mail, win = win, elo = elo)

@app.route("/suprcompte")
def suprcompte():
    return render_template("suprcompte.html")

@app.route("/supr", methods=['POST', 'GET'])
def supr():
    con = connect(join(app.config['DATA_DIR'],'database/compte.db'))
    cur = con.cursor()
    info = cur.execute("SELECT mail, mdp FROM donnee WHERE uuid=?;",(session['uuid'], )).fetchmany()[0]
    if info == (request.form["mail"], request.form["mdp1"]) and request.form["mdp1"] == request.form["mdp2"] and request.form["confirmer"] == "CONFIRMER":
        cur.execute("DELETE FROM stats where uuid=?;",(session['uuid'], ))
        cur.execute("DELETE FROM donnee where uuid=?;",(session['uuid'], ))
        con.commit()
        return redirect("/")
    else:
        return redirect("/suprcompte")

@app.route("/presentation")
def presentation():
    return render_template('presentation.html')

@app.route("/jouer")
def jouer():
    return render_template('jouer.html')

@app.route("/queue", methods=['GET'])
def queue():
    session["last_code"] = None
    session["bot"] = None
    if session.get("uuid") != None: # SI LE JOUEUR EXISTE
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file_read:
            data = load(file_read)
        if data == None:
            data = {"combat":"None"} 
            with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file: 
                dump(data, file)
        if data[request.args.get('gamemode')] == "None": # SI PERSONNE NE QUEUE
            matchuuid= str(uuid4())
            data[request.args.get('gamemode')] = [session["uuid"], matchuuid]
            with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file: 
                dump(data, file)
            session["bot"] = "1"
            session["match"] = matchuuid
        elif data[request.args.get('gamemode')][0] == session["uuid"][0]: # SI UNE MEME PERSONNE QUEUE 2 FOIS
            return redirect("/")
            
        else: # SI LE JOUEUR QUEUE DANS UNE QUEUE DEJA PLEINE
            other_player = data[request.args.get('gamemode')][0]
            session["match"] = data[request.args.get('gamemode')][1]
            data[request.args.get('gamemode')] = "None"
            session["bot"] = "2"
            with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:     
                dump(data, file)   
            with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as file_match:
                dump({"p1":session["uuid"],"p2":other_player, "pos_p1": [0, 0], "pos_p2": [15, 10], "coins": [], "p1_finit":False, "p2_finit":False, "p1_submitted":False, "p2_submitted":False, "shields":[], "dispo":True, "winner":None, "p1_points":0, "p2_points":0}, file_match)        
            return redirect("/combat")
    else:
        return redirect("/")
    return render_template("queue.html", gamemode=request.args.get("gamemode"))

@app.route("/leave_queue")
def leave_queue():
    with open(join(app.config['DATA_DIR'],"matches/queue.json"), "r") as file:
        data = load(file)
    if data[request.args.get("type")][0] == session["uuid"]:
        data[request.args.get("type")] = "None"
        with open(join(app.config['DATA_DIR'],"matches/queue.json"), "w") as file:
            dump(data, file)
    return redirect("/")

@app.route("/combat")
def combat():
    ennemy = '1' if session['bot'] == '2' else '2'
    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
        data_match = load(match_file)
    model = load_map(join(app.config['DATA_DIR'],f'maps/map{randint(1,1)}.csv'), session["match"])

    cmds = None
    if session.get('last_code') != None:
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as match_file:
            dump(data_match, match_file)

        interpreter = EdaExecutor(data_match[f"pos_p{session['bot']}"][0], data_match[f"pos_p{session['bot']}"][1], [])
        cmds = compileur(lexxer(session['last_code']), interpreter)
        for func in cmds:
            in_shield = False
            for s in data_match["shields"]:
                print(s)
                if s[1] == session["bot"]:
                    in_shield = True
                    break 
            
            if in_shield:
                pop_indexes = []
                for i in range(len(data_match["shields"])):
                    if data_match["shields"][i]["bot"] == session["bot"]:
                        data_match["shields"][i]["tour"] -= 1
                        if data_match["shields"][i]["tour"] == -1:
                            pop_indexes.append(i)
                pop_indexes.reverse()
                for index in pop_indexes:
                    data_match["shields"].pop(index)
            else:
                func[0](model["walls"], int(func[1][0]))
            data_match[f"pos_p{session['bot']}"] = [interpreter.memory[pos_x], interpreter.memory[pos_y]]
            data_match["dispo"] = not (session["bot"] == "1")
        for shield in interpreter.memory[shields]:
            data_match["shields"].append(shield)
        data_match[f"p{session['bot']}_finit"] = True
        if data_match[f"pos_p{session['bot']}"] in data_match["coins"]:
            data_match[f"p{session['bot']}_points"] += 1
            data_match["coins"].remove(data_match[f"pos_p{session['bot']}"])
            print(data_match[f"p{session['bot']}_points"])
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as setdispo:
            dump(data_match, setdispo)

        while True:
            with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as check_dispo:
                try:
                    if load(check_dispo)[f"p{ennemy}_finit"]:
                        break
                except decoder.JSONDecodeError:
                    pass
            sleep(0.5)
    else:
        data_match["coins"] = model["coins"]
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as setcoins:
            dump(data_match, setcoins)
    sleep(1)
    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
        data_match = load(match_file)
    map_str = ""
    for x in range(model['w']):
        for y in range(model['h']):
            has_shield = False
            for s in data_match["shields"]:
                if [x, y] == s[0]:
                    has_shield = True

            if [x, y] in model['walls']:
                if has_shield:
                    map_str += SYMB['shield'][0]
                else:
                    map_str += SYMB['wall']
            elif [x, y] in data_match['coins']:
                if has_shield:
                    map_str += SYMB['shield'][1]
                else:
                    map_str += SYMB['coin']
            elif [x, y] == data_match["pos_p1"]:
                map_str += SYMB['bot'][0]
            elif [x, y] == data_match["pos_p2"]:
                map_str += SYMB['bot'][1]
            else:
                if has_shield:
                    map_str += SYMB['shield'][1]
                else:
                    map_str += SYMB['free']
        map_str += "\n"
    data_match[f"p{session['bot']}_submitted"] = False
    data_match[f"p{session['bot']}_finit"] = False
    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as match_file:
        dump(data_match, match_file)
    return render_template('combat.html', map=map_str, bot=session["bot"])

@app.route("/result_game")
def result_game():
    con = connect(join(app.config['DATA_DIR'],'database/compte.db'))
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

@app.route('/refresh', methods=['POST'])
def refresh():
    return redirect("/")

@app.route('/combat/next-turn', methods=['POST'])
def next_turn():
    ennemy = '1' if session['bot'] == '2' else '2'
    with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
        data_match = load(match_file)
    while True:
        data_match[f"p{session['bot']}_submitted"] = True
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "w") as match_file:
            dump(data_match, match_file)
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
            if load(match_file)[f"p{session['bot']}_submitted"]:
                break
    session['last_code'] = ""
    if request.form.get("code") == None:
        session['last_code'] = request.json['text']
    else:
        session['last_code'] = request.form["code"]
    while True:
        with open(join(app.config['DATA_DIR'],f"matches/running/{session['match']}.json"), "r") as match_file:
            try:
                if load(match_file)[f"p{ennemy}_submitted"]:
                    break
            except decoder.JSONDecodeError:
                pass
        sleep(0.5)
    return redirect("/combat")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)