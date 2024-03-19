import csv

SYMB = {
    'wall': ' X ',
    'free': '   ',
    'bot': [' @ ', ' # ']
}

def load_map(map_csv):
    with open(map_csv, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    w = len(data[0])
    h = len(data)

    walls = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '1']
    bot1 = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '2'][0]
    bot2 = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '3'][0]

    bot = {'1' : bot1, '2' : bot2}
    
    return {'w': w,'h': h,'bot' : bot,'walls': walls}

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