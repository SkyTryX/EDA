from __future__ import annotations
from typing import Literal
from json import dump, load
from dataclasses import dataclass

class EdaError(Exception):
    pass

memory = {0:0, 1:0, 2:[]}
pos_x = 0
pos_y = 1
shields = 2

def read_args(code:str)->tuple[str, int]:
    res = [""]
    for _,c in enumerate(code):
        if c == ")":
            return res
        elif c == ",":
            res.append("")
        elif c != " ":
            res[len(res)-1] += c

OP_CODE = Literal['REPEAT', 'GAUCHE', 'DROITE', 'BAS', 'HAUT' 'IFTHENELSE', 'WAIT', 'SHIELD']

class NOOP:
    """the empty ast"""
    pass

@dataclass
class OP:
    op_code: OP_CODE 
    args: tuple[int, list[OP]]



def gauche(walls):
    if not [memory[pos_y],memory[pos_x]-1] in walls or memory[pos_x] == 0:
        memory[pos_x] -= 1

def droite(walls):
    if not [memory[pos_y], memory[pos_x]+1] in walls or memory[pos_x] == 10:
        memory[pos_x] += 1

def bas(walls):
    if not [memory[pos_y]-1, memory[pos_x]] in walls or memory[pos_y] == 0:
        memory[pos_y] += 1

def haut(walls):
    if not [memory[pos_y]+1, memory[pos_x]] in walls or memory[pos_y] == 15:
        memory[pos_y] -= 1

def wait():
    pass

def shield(tour:int):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if j != 0 or i != 0:
                memory[shields].append({(memory[pos_y]+j, memory[pos_x]+i):tour})

def loadi(match:str):
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
            return (shield, [instr.args[0]])
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


def lexxer2(code:list[str|int], res:list[OP]= [], repeat_list:list[list] = []) -> list[OP]:
    if len(code) == 0:
        return res
    in_repeat = False
    if code[0] in ["gauche", "droite", "bas", "haut", "wait", "shield"]:
        for i,c in enumerate(code):
            opened = False
            args = 0
            if c == "(":
                opened = True
            elif type(c) == int and opened:
                args = args*10+int(c)
            elif c == ")":
                if in_repeat:
                    repeat_list[len(repeat_list)-1].append(OP(op_code=code[0], args=(args, [])))
                else:
                    res.append(OP(op_code=code[0], args=(args, [])))
                return lexxer2(code[i:], res, repeat_list)
    elif code[0] == "repeat":
        in_repeat = True
        repeat_list.append([code[2]])
    elif code[0] == "}":
        if len(repeat_list) >= 2:
            repeat_list[len(repeat_list)-1].append(OP(op_code="repeat", args=(repeat_list[len(repeat_list)-1][0], repeat_list[len(repeat_list)-1][1:])))
        else:
            res.append(OP(op_code="repeat", args=(repeat_list[len(repeat_list)-1][0], repeat_list[len(repeat_list)-1][1:])))
        in_repeat = False
        repeat_list.pop(len(repeat_list)-1)
    return lexxer2(code[1:], res, repeat_list)
    

def spliter(code:str)->list[str|int]:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog:list[str] = []
    temp:str = ""
    for c in code:
        temp += c
        if temp in ["gauche", "shield", "droite", "bas", "haut", "wait", "repeat", "(", ")", "{", "}", ";"]:
            prog.append(temp)
            temp = ""
        elif temp.isdigit():
            if type(prog[len(prog)-1]) == int:
                prog[len(prog)-1] = prog[len(prog)-1]*10+int(temp)
            else:
                prog.append(int(temp))   
            temp = ""  
    return prog