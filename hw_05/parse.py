import ply.yacc as yacc
import sys

from lex import tokens

sys_err = False
sys_err_string = ''

"""
Описание логики: 
H  -> A1. | A1  :- E.        H  -  head
E  -> (M + E) | M            E  - expression
M  -> (P * M) | P            M  - disjunction
P  -> A1 | (E)               P  - conjunction
A1 -> L A2 | L               A1 - atom1
A2 -> A1 | (A3) | (A3) A2    A2 - atom2
A3 -> L A2                   A3 - atom3, L - literal
"""


def p_H_A1(p):
    'head : atom1 DOT'
    p[0] = f'{p[1]}, DOT'


def p_H_A1_E(p):
    'head : atom1 TSTILE expression DOT'
    p[0] = f'{p[1]}, TSTILE, {p[3]}, DOT'


def p_E_M_E(p):
    'expression : disjunction PLUS expression'
    p[0] = f'{p[1]}, PLUS, {p[3]}'


def p_E_M(p):
    'expression : disjunction'
    p[0] = f'{p[1]}'


def p_M_P_M(p):
    'disjunction : conjunction MULT disjunction'
    p[0] = f'{p[1]}, MULT, {p[3]}'


def p_M_P(p):
    'disjunction : conjunction'
    p[0] = f'{p[1]}'


def p_P_A1(p):
    'conjunction : atom1'
    p[0] = f'{p[1]}'


def p_P_E(p):
    'conjunction : LBR expression RBR'
    p[0] = f'LBR, {p[2]}, RBR'


def p_A1_L_A2(p):
    'atom1 : LIT atom2'
    p[0] = f'{p[1]}, {p[2]}'


def p_A1_L(p):
    'atom1 : LIT'
    p[0] = f'{p[1]}'


def p_A2_A1(p):
    'atom2 : atom1'
    p[0] = f'{p[1]}'


def p_A2_A3(p):
    'atom2 : LBR atom3 RBR'
    p[0] = f'LBR, {p[2]}, RBR'


def p_A2_A3_A2(p):
    'atom2 : LBR atom3 RBR atom2'
    p[0] = f'LBR, {p[2]}, RBR, {p[4]}'


def p_A3_L_A2(p):
    'atom3 : LIT atom2'
    p[0] = f'{p[1]}, {p[2]}'


def p_error(p):
    global sys_err
    global sys_err_string
    sys_err = True
    sys_err_string = "Syntax error"


parser = yacc.yacc()

while True:
    try:
        s = input("calc> ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    if sys_err:
        print(sys_err_string)
        sys_err = False
    else:
        print(result)
