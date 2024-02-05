#explication jeu

dans le server :
    on a un model ou par exemple -> map(mur, loot, vide) 
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
creer un rafrechissement de la page html pour pouvoir suivre le combats des robots sans devoir refresh la page naturelement
render(model) -> str et cette str et passer a un render_template