import ply.yacc as yacc
import sys

from lex import tokens

sys_err = False
sys_err_string = ''


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
    sys_err_string = "Syntax error\n"


parser = yacc.yacc()


def main():
    global sys_err
    global sys_err_string
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
    i = 0
    prev_pos = 0
    file_out = open(out_file_name, 'w')  # open output file
    while i < len(s):
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = parser.parse(current_expression)
        if sys_err:
            file_out.write(sys_err_string)
            sys_err = False
        else:
            file_out.write(result + '\n')
        prev_pos = i


if __name__ == "__main__":
    main()
