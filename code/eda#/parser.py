expressions:dict[str, str]= {
    "right()":"right",
    "left()":"left",
    "jump()":"jump",
}

def compiler(txt:str) -> list:
    res = []
    repeating = False
    temp = ""
    for c in txt:
        temp+= c
        # Fin d'instrution
        if c == ";":
            temp = ""
        # Enregistrer instruction
        if expressions.get(temp) != None:
            res.append(expressions.get(temp))
        # Enregistrer boucle
        elif temp == "repeat(":
            res.append({"repeat":0})
            repeating = True
        # Gérer les boucles
        elif repeating:
            try:
                res[len(res)-1]["repeat"] = res[len(res)-1]["repeat"]*10+int(c)
            except ValueError:
                if temp.endswith("){"):
                    repeating = False
                    temp = ""
        # Fin de boucle
        if c == "}":
            res.append("endrepeat")
    return res

print(compiler("right();left();jump();"))
print(compiler("repeat(5){right();}"))
