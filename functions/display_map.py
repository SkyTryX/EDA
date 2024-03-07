import csv

def load_map(map_csv):
    with open(map_csv, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    w = len(data[0])
    h = len(data)

    data = [[int(cell) for cell in row] for row in data]

    SYMB = {
        0: 'free',
        1: 'wall',
        2: 'bot1',
        3: 'bot2'
    }
    model = [[SYMB[value] for value in row] for row in data] 
    return model

def deplacemennt(dico, position_bot : list[tuple], namebot):
    """
    Renvoi le dico modifié si le bot peut se déplacer au bon endroit, sinon renvoi le même dico
    exemple de fonction ecrite : deplacement( load_map(map1.csv), (2,6), '1' )
    """
    for x in dico['wall'][0]:
        # manque de définir pour que le bot sorte pas de la map
        if position_bot == x:
            return dico, False
        else:
            dico[namebot] = [position_bot]
            return dico, True


