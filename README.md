# Trophées NSI
## Répartition des taches
- Design du site (CSS, Bootstrap) **Evann**
- Structure du site (HTML) **Alexis**
- Creation du moteur graphique du jeu (HTML/JS) **Evann Alexis**
- Game design **Evann Alexis**
- Creation système de jeu:
    Resultat **Alexis**
    Déroulement **Alexis Evann Dorian**
    Queue **Dorian**
- Creation du language de programation EDA (design du language et création d'un parser) **Dorian**
- Création d'une data base, de profile et de stats **Alexis Dorian**
- Création d'un système de modération **Dorian**
- Journal **Alexis Evann Dorian**
- Doc Technique **Dorian**
- PDF **Alexis**
- Vidéo:
    Montage
    Script
    Organisation (où, avec quoi?)
- Deployer le projet **Dorian**

1) Design du site
Couleure principale/secondaire: Style console/violet noir
fond d'écran : Noir
police ecriture : Vielle police de console (violette)

2) Structure du site
- Page Main (Titre ,lien presentation, login/register, coordonnées etc...)
- Page Presentation équipe et des dossiers techniques etc... (lien vidéo, doc technique, doc pdf, résumé)
- Page de register/Login (mail, ign, password, confirm password // mail/ign password mdp oublié)
- Page de profile (stats (win, kills, elo, map favori), modif password, mail, pseudo, suppr compte etc...)
- Peut-être -> Page modération (menu avec tout les joueurs, pouvoir les bannir, suppr leur compte, changer leur donnée) 
- Page de selection du mode de jeu (Combat)
- Page de jeu (avec moteur graphique Canvas et champ d'entrée du code EDA#)
- page de resultat de la game (stats, etc...)

3) Creation moteur graphique
En Ascii avec couleur ( comme pour le texte ça sera violet )

4) Game design
**Global**
Chaque instruction s'execute 1 à 3 fois d'affilés, en même quantitée pour chaque equipe.

**1v1**
But: Destruire le robot adverse et/ou recuperer les pièces (le gagnant est le dernier survivant, si aucun robot n'est détruit, celui qui a récolté le plus de pièces gagne)
Idées map: Desert (Plat), Forêt(Labyrinthique), Ville (Entre les deux)

5) Système de jeu
**Map**
dans le serveur :
    on a un model ou par exemple -> map(mur, pièce, vide) 
    qui donne des caracteristique au fichier de la map(peut etre un .txt, .csv) ecrit avec des nombres
    exemple -> mur = 1, loot = 2, vide = 0
    la carte en .csv sera avec des 1,2 et des 0

    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 -> ligne1
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne2
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne3
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne4
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne5
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne6
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -> ligne7
    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 -> ligne8

return render_template("jeu.html", map = " ligne1 \n ligne2 \n)
creer un rafrechissement de la page html pour pouvoir suivre le combats des robots sans devoir refresh la page manuellement
render(model) -> str et cette str et passer a un render_template

6) EDA#
- droite(int);
- gauche(int);
- haut(int);
- bas(int);
- shield(int); -> crée un bouclier de 1 case tt autour qui détruit le robot enemi si il rentre dedans, en contrepartie on ne peux pas bouger pendant l'activation, c'est le seul moyen de détruire un robot.
- repeat(int){action(s);};

7) Création d'une database
**donnee**
uuid PRIMARY_KEY
mail 
pseudo
mdp
admin

**stat**
uuid PRIMARY_KEY FOREIGN_KEY
win
elo

8) Système de modération
Peut-être -> Si admin = 1, tu peux accéder à un panel admin, qui te permet de voir le profil d'un joueur, de le bannir, supprimer son compte etc...
