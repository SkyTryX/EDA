from math import log10

def compiler(code:str) -> list:
    memory = []
    repeat = False
    temp = ""
    repeat_time = 0
    for b in code:
        temp+=b
        if repeat:
            if b == ")":
                repeat = False
                repeat_time = memory[len(memory)][1]
            elif memory[len(memory)][0] == "repeat":
                memory[len(memory)][1] = memory[len(memory)][1]+(int(b)*log10(memory[len(memory)][1]))
            else:
                memory.append(["repeat", b])
        elif temp == "repeat(":
            repeat = True
            temp = ""
        if temp == "avance()":
            if memory[len(memory)][0] == ">":
                ...

