import sys

from parsita import *
from collections import namedtuple
from parsita.util import constant
from parsita.util import splat


class PrologParser(TextParsers, whitespace='[ \t\n]*'):
    module = lit('module') > constant("module")
    literal = reg(r'[A-Za-z_][A-Za-z_0-9]*') > (lambda x: ["Atom", str(x)])
    identificator = reg(r'[a-z_][a-z_0-9]*') > (lambda x: ["ID", str(x)])
    disunction = lit(';') > constant("DIS")
    conjunction = lit(',') > constant("CON")
    dot = lit('.') > constant("DOT")
    lbr = lit('(')
    rbr = lit(')')
    tstile = lit(':-') > constant("TSTILE")
    # ---------------------------------------------------------------
    mod = module & identificator & dot
    # ---------------------------------------------------------------
    head = atom1 & tstile & expression & dot | atom1 & dot
    expression = M & disunction & expression | M
    M = P & conjunction & M | P
    P = lbr & expression & rbr | atom1
    atom1 = literal & atom2 | literal
    atom2 = lbr & atom3 & rbr & atom2 | atom1 | lbr & atom3 & rbr
    atom3 = atom1 | lbr & atom3 & rbr
    # ----------------------------------------------------------------


def print_result(result, file_out):
    result = result.replace(')', '')
    result = result.replace('(', '')
    result = result.replace('\'', '')
    result = result.replace(',', '')
    result = result.replace('[', '(')
    result = result.replace(']', ')')
    result = result.replace('"', '')
    result = result.replace('( (', '((')
    result = result.replace(') )', '))')
    file_out.write(result[8:len(result) - 1] + '\n')


def main():
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
        result = str(PrologParser.mod.parse(current_expression))
        if result[:7] == "Success":
            print_result(result, file_out)
        else:
            result = str(PrologParser.head.parse(current_expression))
            if result[:7] == "Success":
                print_result(result, file_out)
            else:
                file_out.write("Syntax error!\n")
        prev_pos = i


if __name__ == "__main__":
    main()
