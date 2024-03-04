import csv
import os

def load_map(map_csv):

    try:
        with open(os.path.abspath(map_csv), 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        print(f"Error: Map file '{map_csv}' not found.")
        return None
    except PermissionError:
        print(f"Error: Map file '{map_csv}' cannot be accessed.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    if not data:
        print("Error: Map is empty.")
        return None

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

def display(model, symbols={"wall": "*", "free": " ", "bot": ["@", "#"]}):
    if not model or not model['bots']:
        print("Error: Map is empty or has no bots.")
        return

    for y in range(model['h']):
        line = []
        for x in range(model['w']):
            if (x,y) in model['walls']:
                line.append(symbols["wall"])
            elif (x,y) in model['bots']:
                line.append(symbols["bot"][model['bots'].index((x,y))])
            else:
                line.append(symbols["free"])
        print("".join(line))

def render(model):
    if model:
        display(model)
    else:
        print("Error: Model is empty or has no bots.")

model = load_map('map.csv')
render(model)