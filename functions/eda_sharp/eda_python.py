from eda_assembly import OP, read_args
from json import dump, load

def gauche(p:str, match:str):
    print("GAUCHE")
    with open(match+".json", "r") as file_read:
        data = load(file_read)
        data["pos_"+p][0] -= 1
    with open(match+".json", "w") as file_write:
        dump(data, file_write)

def droite(p:str, match:str):
    print("DROITE")
    with open(match+".json", "r") as file_read:
        data = load(file_read)
        data["pos_"+p][0] += 1
    with open(match+".json", "w") as file_write:
        dump(data, file_write)

def bas(p:str, match:str):
    print("BAS")
    with open(match+".json", "r") as file_read:
        data = load(file_read)
        data["pos_"+p][1] += 1
    with open(match+".json", "w") as file_write:
        dump(data, file_write)

def haut(p:str, match:str):
    print("HAUT")
    with open(match+".json", "r") as file_read:
        data = load(file_read)
        data["pos_"+p][1] -= 1
    with open(match+".json", "w") as file_write:
        dump(data, file_write)

def wait(p:str, match:str):
    print("WAIT")
    pass

def shield(p:str, match:str, tour:int):
    print("SHIELD " + tour)
    with open(match+".json", "r") as file_read:
        data = load(file_read)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != j:
                    data["shield"].append({(data["pos_"+p][0]+i, data["pos_"+p][1]+j):tour})
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