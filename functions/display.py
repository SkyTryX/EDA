import csv

def load_map(map_csv):
    with open(map_csv, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    w = len(data[0])
    h = len(data)

    walls = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '1']
    bots = [(x, y) for y in range(h) for x in range(w) if data[y][x] in ['2', '3']]

    model = {
        'w': w,
        'h': h,
        'bots': bots,
        'walls': walls
    }

    return model

def display(model):
    SYMB = {
        'wall': '*',
        'free': ' ',
        'bot': ['@', '#']
    }

    for y in range(model['h']):
        line = []
        for x in range(model['w']):
            if (x,y) in model['walls']:
                line.append(SYMB['wall'])
            elif (x,y) in model['bots']:
                line.append(SYMB['bot'][model['bots'].index((x,y))])
            else:
                line.append(SYMB['free'])
        print("".join(line))

def render(model):
    display(model)

model = load_map('map.csv')
render(model)
