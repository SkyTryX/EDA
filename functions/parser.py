expressions:dict[str, str]= {
    "move(":{"move":[]},
    "attack(":{"attack":[]},
    "wait()":"wait",
    "take()":"take"
}

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
                            res[len(res)-1][list(res[len(res)-1].keys())[0]].append(c)
                        else:
                            res[len(res)-1][list(res[len(res)-1].keys())[0]][index] += c
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
