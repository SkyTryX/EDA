# trophee-nsi
## Jeu style Pyrate en mode versus

Liste des pages: 
- Page Main
- Presentation équipe et des dossiers techniques etc...
- Page de register/Login
- Page de profile (stats, modif password, mail, pseudo, suppr compte etc...)
- Page modération (pour bannir les gens qui utilisent des scripts...)
- Page de selection du mode de jeu (Course,1v1, 2v2, tournois?)
- Page de jeu (avec moteur graphique Canvas et champ d'entrée du code EDA#)
- page de resultat de la game (stats, etc...)

Le serveur execute les programmes des differents en parallèle.

### Répartition des taches
- Design du site (CCS, Bootstrap?) **Evann**
- Creation du moteur graphique du jeu (HTML/JS) **Evann**
- Game design **Evann Alexis**
- Creation système de jeu (résultat, déroulement du jeu, queue)
- Creation du language de programation EDA (design du language et création d'un parser) **Dorian**
- Création d'une data base, de profile et de stats **Alexis**
- Création d'un système de modération **Dorian**
- Journal **Alexis**
- Résumé **Tout le monde**
- Doc Technique **Dorian**
- PDF **Alexis**
- Vidéo **Tout le monde**
- Deployer le projet **Dorian**

**EDA#**
- move(up/down/right/left)
- attack(normal/special??)
- wait(1) (en seconde)
- from 0 to 10 (i) (for i in range(0, 10)) > on peut rien mettre entre from to  pour i=0
- même while et if que python
- endfor endwhile endif
- var = 0,True/False pas de string et float
- QUE des elements de prog qui sert à quelques choses pour le jeu