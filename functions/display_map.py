import csv

def load_map(map_csv):
    with open(map_csv, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    w = len(data[0])
    h = len(data)

    walls = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '1']
    bot1 = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '2']
    bot2 = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '3']

    bot = {'1' : bot1, '2' : bot2}
    
    return {'w': w,'h': h,'bot' : bot,'walls': walls}

