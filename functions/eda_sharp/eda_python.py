from eda_assembly import OP, read_args
from json import dump, load

memory = {0:0, 1:0, 2:[]}
pos_x = 0
pos_y = 1
shields = 2

def gauche():
    print("GAUCHE")
    memory[pos_x] -= 1

def droite():
    memory[pos_x] += 1

def bas():
    memory[pos_y] += 1

def haut():
    memory[pos_y] -= 1

def wait():
    pass

def shield(tour:int):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != j:
                memory[shields].append({(memory[pos_x]+i, memory[pos_y]+j):tour})

def load(match:str):
    with open(match+".json", "r") as file_read:
        return load(file_read)

def save(p:str, match:str, data:dict):
    data["pos_"+p]= [memory[pos_x], memory[pos_y]]
    with open(match+".json", "w") as file_write:
        dump(data, file_write)


def lexxer(code:str)->list[OP]:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog:list[OP] = []
    temp:str = ""
    repeating:bool = False
    repeat_list:list[list] = []
    for i,c in enumerate(code):
        temp += c
        if temp == "shield(":
            a = read_args(code[i+1:])
            if repeating:
                repeat_list[len(repeat_list)-1].append(OP(op_code='shield', args=(a[0], [])))
            else:
                prog.append(OP(op_code='shield', args=(a[0], [])))
        elif temp in ["gauche()", "droite()", "bas()", "haut()", "wait()"]:
            if repeating:
                repeat_list[len(repeat_list)-1].append(OP(op_code=temp.removesuffix("()"), args=(0, [])))
            else:
                prog.append(OP(op_code=temp.removesuffix("()"), args=(0, [])))
        elif c in ["{",";"]:
            temp = ""
        elif temp == "repeat(":
            a = read_args(code[i+1:])
            repeat_list.append(a)
            repeating = True
        elif c == "}":
            if len(repeat_list) >= 2:
                repeat_list[len(repeat_list)-1].append(OP(op_code="repeat", args=(repeat_list[len(repeat_list)-1][0], repeat_list[len(repeat_list)-1][1:])))
            else:
                prog.append(OP(op_code="repeat", args=(repeat_list[len(repeat_list)-1][0], repeat_list[len(repeat_list)-1][1:])))
            repeat_list.pop(len(repeat_list)-1)
            repeating = False
            temp = ""
    return prog

def parser(instr:OP):
    match instr.op_code:
        case "gauche":
            return (gauche, [])
        case "droite":
            return (droite, [])
        case "haut":
            return (haut, [])
        case "bas":
            return (bas, [])
        case "wait":
            return (wait, [])
        case "shield":
            return (wait, [instr.args[0]])
        case "repeat":
            res = parser(instr.args[1][0])
            instr.args[1].pop(0)
            return res

        

def compileur(prog:list[OP]) -> list[tuple]:
    res = []
    for instr in prog:
        if instr.op_code == "repeat":
            repeat = []
            while len(instr.args[1]) != 0:
                repeat.append(parser(instr))
            for i in range(int(instr.args[0])):
                res += repeat
        else:
            res.append(parser(instr))
    return res

print(compileur(lexxer("repeat(3){wait();}gauche();droite();")))