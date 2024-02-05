import ply.yacc as yacc
from lexxer import tokens

def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]

operations = {
'+' : lambda x , y : x+y ,
'-' : lambda x , y : x-y ,
'*' : lambda x , y : x*y ,
'/' : lambda x , y : x/y ,
}

def p_expression_op(p):
    '''
    expression : expression PLUS expression 
    | expression MINUS expression
    | expression MULT expression
    | expression DIV expression
    ''' 
    p[0] = operations[p[2]](p[1], p[3])

precedence = (('left', 'PLUS'), ('left', 'MINUS'), ( 'left', 'MULT'), ('left', 'DIV'))

def p_error(p):
    print(f"Syntax error in line {p.lineno}")
    yacc.errok()

yacc.yacc(write_tables=False)
if __name__ == "__main__":
    print(yacc.parse("3*2+1"))