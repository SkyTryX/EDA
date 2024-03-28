from __future__ import annotations
from typing import Literal
from dataclasses import dataclass

OP_CODE = Literal['REPEAT', 'GAUCHE', 'DROITE', 'BAS', 'HAUT' 'IFTHENELSE', 'WAIT', 'SHIELD']

class NOOP:
    """the empty ast"""
    pass

@dataclass
class OP:
    op_code: OP_CODE 
    args: tuple[int, list[OP]]

pos_x = 0
pos_y = 1
shields = 2

class EdaExecutor():
    

    def __init__(self, x, y, shields) -> None:
        self.memory = {0:x, 1:y, 2:shields}
        
    def bas(self, walls, i):
        if not [self.memory[pos_y],self.memory[pos_x]-i] in walls or self.memory[pos_x] == 10:
            self.memory[pos_x] += i

    def haut(self, walls, i):
        if not [self.memory[pos_y], self.memory[pos_x]+i] in walls or self.memory[pos_x] == 0:
            self.memory[pos_x] -= i

    def gauche(self, walls, i):
        if not [self.memory[pos_y]-i, self.memory[pos_x]] in walls or self.memory[pos_y] == 0:
            self.memory[pos_y] -= i

    def droite(self, walls, i):
        if not [self.memory[pos_y]+i, self.memory[pos_x]] in walls or self.memory[pos_y] == 15:
            self.memory[pos_y] += i

    def wait(self, walls, i):
        pass

    def shield(self, walls, tour:int):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if j != 0 or i != 0:
                    self.memory[shields].append([[self.memory[pos_y]+j, self.memory[pos_x]+i],tour])


def read_args(code:str)->tuple[str, int]:
    res = [""]
    for _,c in enumerate(code):
        if c == ")":
            return res
        elif c == ",":
            res.append("")
        elif c != " ":
            res[len(res)-1] += c

def lexxer2(code:str)->list[OP]:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog:list[OP] = []
    temp:str = ""
    repeating:bool = False
    repeat_list:list[list] = []
    for i,c in enumerate(code):
        temp += c
        if temp in ["shield(","gauche(", "droite(", "bas(", "haut(", "wait("]:
            a = read_args(code[i+1:])
            if repeating:
                repeat_list[len(repeat_list)-1].append(OP(op_code='shield', args=(a[0], [])))
            else:
                prog.append(OP(op_code='shield', args=(a[0], [])))
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

def lexxer(code:str)->list[OP]:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog:list[OP] = []
    temp:str = ""
    repeating:bool = False
    for i,c in enumerate(code):
        temp += c
        if temp in ["shield(","gauche(", "droite(", "bas(", "haut(", "wait("]:
            a = read_args(code[i+1:])
            if repeating:
                prog[len(prog)-1].args[1].append(OP(op_code=temp.removesuffix("("), args=(int(a[0]), [])))
            else:
                prog.append(OP(op_code=temp.removesuffix("("), args=(a[0], [])))
        elif c in ["{",";"]:
            temp = ""
        elif temp == "repeat(":
            a = read_args(code[i+1:])
            if repeating:
                 prog[len(prog)-1].args[1].append(OP(op_code="repeat", args=(int(a[0]), [])))
            else:
                prog.append(OP(op_code="repeat", args=(int(a[0]), [])))
            repeating = True
        elif c == "}":
            repeating = False
            temp = ""
    return prog

def parser(instr:OP, interpreter:EdaExecutor):
    match instr.op_code:
        case "gauche":
            return (interpreter.gauche, [instr.args[0]])
        case "droite":
            return (interpreter.droite, [instr.args[0]])
        case "haut":
            return (interpreter.haut, [instr.args[0]])
        case "bas":
            return (interpreter.bas, [instr.args[0]])
        case "wait":
            return (interpreter.wait, [instr.args[0]])
        case "shield":
            return (interpreter.shield, [instr.args[0]])
        case "repeat":
            res = parser(instr.args[1][0])
            instr.args[1].pop(0)
            return res


def compileur(prog:list[OP], interpreteur:EdaExecutor) -> list[tuple]:
    res = []
    for instr in prog:
        if instr.op_code == "repeat":
            repeat = []
            while len(instr.args[1]) != 0:
                repeat.append(parser(instr, interpreteur))
            for i in range(int(instr.args[0])):
                res += repeat
        else:
            res.append(parser(instr, interpreteur))
    return res

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