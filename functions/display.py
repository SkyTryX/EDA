"""
transforme le modÃ¨le en asciimage
"""
model = {
    'w':6,
    'h':4,
    'bots': [(2, 1),(3,2)],
    'walls': [(1, 1), (1, 2), (1, 3), (2, 3), (4,0), (4, 1), (4, 3), (4, 4)]
}

SYMB = {
    'wall': '*',
    'free': ' ',
    'bot': ['@', '#']
}

def render(mod):
    with open('data.txt', 'w') as f:
        f.write('')
    with open('data.txt','a') as f:
        for y in range(mod['h']):
            line = []
            for x in range(mod['w']):
                if (x,y) in mod['walls']:
                    line.append(SYMB['wall'])
                elif (x,y) in mod['bots']:
                    line.append(SYMB['bot'][mod['bots'].index((x,y))])
                else:
                    line.append(SYMB['free'])
            print(line)
            f.write("".join(line)+"\n")


render(model)