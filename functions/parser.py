expressions:dict[str, str]= {
    "move(":{"move":[]},
    "attack(":{"attack":[]},
    "wait()":"wait",
    "take()":"take"
}

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    return True

def lexxer(txt:str) -> list:
    reading_input = False
    res= []
    for i in txt.split(";"):
        temp = ""
        index = 0
        for c in i:
            temp+= c
            if reading_input:
                if c == ",":
                    index += 1
                elif c == ")":
                    reading_input = False
                elif c != " ":
                    if type(res[len(res)-1]) == dict:
                        if len(res[len(res)-1][list(res[len(res)-1].keys())[0]]) == index:
                            if represents_int(c):
                                res[len(res)-1][list(res[len(res)-1].keys())[0]].append(int(c))
                            else:
                                res[len(res)-1][list(res[len(res)-1].keys())[0]].append(c)
                        else:
                            if represents_int(res[len(res)-1][list(res[len(res)-1].keys())[0]][index]):
                                res[len(res)-1][list(res[len(res)-1].keys())[0]][index] = res[len(res)-1][list(res[len(res)-1].keys())[0]][index]*10+int(c)
                            else:
                                res[len(res)-1][list(res[len(res)-1].keys())[0]][index] += res[len(res)-1][list(res[len(res)-1].keys())[0]][index]
            if expressions.get(temp) != None:
                # Je fais ça au lieu d'utiliser expression car sinon ca écrit dans la variable expressions
                if temp == "move(":
                    res.append({"move":[]})
                elif temp == "attack(":
                    res.append({"attack":[]})
                elif temp == "wait()":
                    res.append("wait")
                elif temp == "take()":
                    res.append("take"),
                reading_input = True
    return res

def unthreader(txt:str) -> str:
    reading_repeat= False
    repeat_number = None
    reading = True
    res = ""
    index = -1
    for c in txt:
        index += 1
        if reading_repeat:
            if c == ")":
                reading_repeat = False
            elif repeat_number == None:
                repeat_number = int(c)
            else:
                repeat_number = repeat_number*10+int(c)
        elif res.endswith("repeat"):
            res = res.removesuffix("repeat")
            reading = False
            reading_repeat = True
        elif c == "{":
            start_index = index+1
        elif c == "}":
            repeating = ""
            for i in range(start_index, index):
                repeating+=txt[i]
            for i in range(repeat_number):
                res+=repeating
            reading = True
        elif reading:
            res+= c
    return res

def eda_sharp(txt:str)->list:
    return lexxer(unthreader(txt))