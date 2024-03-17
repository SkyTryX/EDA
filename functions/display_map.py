import csv
import threading
import time
import json

def move_bot(bot_num, bot, walls, lock, socket):
    with lock:
        if bot:
            for _ in range(2):
                bot[0] = (bot[0][0], bot[0][1] - 1)
                time.sleep(2)
                if socket is not None:
                    socket.send(json.dumps({'type': 'map', 'map': bot}))

def load_map(map_csv, socket=None):
    with open(map_csv, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    w = len(data[0])
    h = len(data)

    walls = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '1']
    bot1 = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '2']
    bot2 = [(x, y) for y in range(h) for x in range(w) if data[y][x] == '3']

    bot = {'1' : bot1, '2' : bot2}
    lock = threading.Lock()
    if socket is not None:
        threading.Thread(target=move_bot, args=(2, bot['2'], walls, lock, socket)).start()
    else:
        move_bot(2, bot['2'], walls, lock, None)

    if socket is not None:
        socket.send(json.dumps({'type': 'map', 'map': bot}))

    return {'w': w,'h': h,'bot' :bot,'walls': walls}

