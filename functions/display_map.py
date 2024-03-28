from csv import reader
from random import randint, seed


SYMB = {
    'wall': ' X ',
    'free': '   ',
    'bot': [' @ ', ' # '],
    'coin':' 0 ',
    'shield': [' $ ', ' . ']
}

def load_map(map_csv, s):
    with open(map_csv, 'r') as file:
        readed = reader(file)
        data = [row for row in readed]

    w = len(data[0])
    h = len(data)

    walls = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '1']
    bot1 = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '2'][0]
    bot2 = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '3'][0]
    seed(s)
    coins = [[x, y] for y in range(h) for x in range(w) if data[y][x] == '0' and randint(0, 10) == 1]
    
    return {'w': w,'h': h,'bot' : {'1' : bot1, '2' : bot2},'walls': walls, "coins":coins}