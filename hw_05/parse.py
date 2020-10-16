import ply.yacc as yacc
import sys

sys_err = False
sys_err_string = ''
s = ''
row_num = 1

import ply.lex as lex

tokens = [
    'LIT',
    'DIS',
    'CON',
    'LBR',
    'RBR',
    'DOT',
    'TSTILE'
]

t_LIT = r'[A-Za-z_][A-Za-z_0-9]*'
t_DIS = r'\;'
t_CON = r'\,'
t_DOT = r'\.'
t_LBR = r'\('
t_RBR = r'\)'
t_TSTILE = r':-'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def find_column(token):
    line_start = s.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    global sys_err_string
    global sys_err
    sys_err_string = "Illegal character: \"" + t.value[0] + "\". Error in line " + str(row_num) + ", colon " + str(
        find_column(t)) + "."
    sys_err = True
    t.lexer.skip(1)


lexer = lex.lex()


def p_H_A1(p):
    'head : atom1 DOT'
    p[0] = f'{p[1]}, DOT'


def p_H_A1_E(p):
    'head : atom1 TSTILE expression DOT'
    p[0] = f'{p[1]}, TSTILE, {p[3]}, DOT'


def p_E_M_E(p):
    'expression : disjunction DIS expression'
    p[0] = f'{p[1]}, DIS, {p[3]}'


def p_E_M(p):
    'expression : disjunction'
    p[0] = f'{p[1]}'


def p_M_P_M(p):
    'disjunction : conjunction CON disjunction'
    p[0] = f'{p[1]}, CON, {p[3]}'


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


def p_A3_A1(p):
    'atom3 : atom1'
    p[0] = f'{p[1]}'


def p_A3_A3(p):
    'atom3 : LBR atom3 RBR'
    p[0] = f'LBR, {p[2]}, RBR'


def p_error(p):
    global sys_err
    global sys_err_string
    sys_err = True
    sys_err_string = "Syntax error!\n"


parser = yacc.yacc()


def main():
    global s
    global sys_err
    global sys_err_string
    global row_num
    in_file_name = sys.argv[1]  # input file
    i = 0
    dot_ix = 0
    while i < len(in_file_name):
        if in_file_name[i] == '.':
            dot_ix = i
        i += 1
    out_file_name = in_file_name[:-(len(in_file_name) - dot_ix - 1)] + "out"  # output file
    file_in = open(in_file_name)  # open file
    s = str(file_in.read())  # read file
    if s[len(s) - 1] == '\n':
        s = s[:-1]
    i = 0
    prev_pos = 0
    file_out = open(out_file_name, 'w')  # open output file
    while i < len(s):
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = parser.parse(current_expression)
        prev_len = len(current_expression)
        current_expression = current_expression.replace('\n', '')
        row_num += prev_len - len(current_expression)
        if sys_err:
            file_out.write(sys_err_string)
            sys_err = False
        else:
            file_out.write(result + '\n')
        prev_pos = i


if __name__ == "__main__":
    main()
