import ply.lex as lex

tokens = (
"NUMBER",
"PLUS",
"MINUS",
"MULT",
"DIV"
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'


def t_NUMBER(t):
    r'\d+'
    if t.value.rfind(".") == -1:
        t.value = int(t.value)
    else:
        t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    lex.input("1*1")
    while True:
        tok = lex.token()
        if not tok : break
        print(f"line {tok.lineno}:{tok.type} ({tok.value})")
