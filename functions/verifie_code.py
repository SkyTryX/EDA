eda = ["repeat", "gauche", "droite", "bas", "haut", "shield", "wait"]
eda_error = "Actions possibles ( pensez à verifier les erreurs de syntaxe) : repeat, gauche, droite, bas, haut, shield, wait"
model_repeat = ["(", int, ")", "{", "}",";"]
model = ["(", int, ")",";"]
model_repeat_error = "Voici comment vous devriez écrire votre code : repeat(int){instruction(s);};"
model_error = "Voici comment vous devriez écrire votre code : action(int);"
gauche = ["(", int, ")",";"]
droite = ["(", int, ")",";"]
bas = ["(", int, ")",";"]
haut = ["(", int, ")",";"]
shield = ["(", int, ")",";"]

def eda_linter(code):
    if len(code) <= 0:
        return [True,None]
    if code[0] not in eda:
        return [False, eda_error]
    else:
        if code[0] in ["gauche", "droite", "bas", "haut", "shield"]:
            if not len(code) >= 5:
                return [False,model_error]
            for x in range(len(model)):
                if model[x] != type(code[x+1]) and model[x] != code[x+1]:
                    return [False,model_error]
            return eda_linter(code[(len(model)+1):])
        if code[0] == "repeat":
            if "}" not in code:
                return [False, model_repeat_error]
            if "{" not in code:
                return  [False, model_repeat_error]
            elif "{" in code and "}" in code:
                code_repeat = code.copy()
                code_repeat = code_repeat[code.index("{")+1:code.index("}")]
                if len(code_repeat)%5 != 0: 
                    return  [False, model_repeat_error]
                else:
                    for x in range(len(code_repeat)//5):
                        if code_repeat[0] in eda:
                                code_repeat = code_repeat[1:]
                        else:
                            return  [False, model_repeat_error]
                        for x in range(len(model)):
                                if model[x] != type(code_repeat[x]) and model[x] != code_repeat[x]:
                                        return [False, model_repeat_error]
                        code_repeat = code_repeat[4:]
            return eda_linter(code[code.index("}")+2:])
            

def spliter(code:str)->list[str|int]:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog:list[str] = []
    temp:str = ""
    for c in code:
        temp += c
        if c in ["(", ")", "{", "}", ";"]:
            if temp != c:
                prog.append(temp.removesuffix(c))
                prog.append(c)
                temp = ""
        elif temp.isdigit():
            if type(prog[len(prog)-1]) == int:
                prog[len(prog)-1] = prog[len(prog)-1]*10+int(temp)
            else:
                prog.append(int(temp))   
            temp = ""
    if temp != "": prog.append(temp)  
    return prog 