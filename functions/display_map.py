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