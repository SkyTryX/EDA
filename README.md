# Trophées NSI
## Répartition des taches
- Design du site (CSS, Bootstrap) **Evann**
- Structure du site (HTML) **Alexis**
- Creation du moteur graphique du jeu (HTML/JS) **Evann**
- Game design **Evann Alexis**
- Creation système de jeu:
    Resultat
    Déroulement
    Queue
- Creation du language de programation EDA (design du language et création d'un parser) **Dorian**
- Création d'une data base, de profile et de stats **Alexis**
- Création d'un système de modération **Dorian**
- Journal **Alexis**
- Doc Technique **Dorian**
- PDF **Alexis**
- Vidéo:
    Montage
    Script
    Organisation (où, avec quoi?)
- Deployer le projet **Dorian**

1) Design du site
Couleure principale/secondaire: Style console/vert blanc
fond d'écran : Noir
police ecriture : Vielle police de console

2) Structure du site
- Page Main (Titre ,lien presentation, login/register, coordonnées etc...)
- Page Presentation équipe et des dossiers techniques etc... (lien vidéo, doc technique, doc pdf, résumé)
- Page de register/Login (mail, ign, password, confirm password // mail/ign password mdp oublié)
- Page de profile (stats (win, kills, elo, map favori), modif password, mail, pseudo, suppr compte etc...)
- Page modération (menu avec tout les joueurs, pouvoir les bannir, suppr leur compte, changer leur donnée)
- Page de selection du mode de jeu (Course,1v1, 2v2, tournois?)
- Page de jeu (avec moteur graphique Canvas et champ d'entrée du code EDA#)
- page de resultat de la game (stats, etc...)

3) Creation moteur graphique
En Ascii avec couleur

4) Game design
**Global**
Chaque instruction s'execute 1 à 3 fois d'affilés, en même quantitée pour chaque equipe.

**1v1**
But: Destruire le robot adverse
Map: Desert (Plat), Forêt(Labyrinthique), Ville (Entre les deux)

5) Système de jeu
...

6) EDA#
- move(up/down/right/left);
- attack(corpsàcorps/distance, up/down/right/left);
- wait();
- take();
- repeat(int){INSTR}

7) Création d'une database
**donnee**
mail PRIMARY_KEY
pseudo
mdp
admin

**stat**
pseudo PRIMARY_KEY FOREIGN_KEY
win
elo

8) Système de modération
...