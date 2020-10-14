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


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
