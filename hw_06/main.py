import sys

from parsita import *
from parsita.util import constant


class PrologParser(TextParsers, whitespace='[ \t\n]*'):
    module = lit('module') > constant("module")
    literal = reg(r'[A-Za-z_][A-Za-z_0-9]*') > (lambda x: ["Atom", str(x)])
    id = reg('[a-zA-Z_][a-zA-Z_0-9]*') > (lambda x: ["ID", str(x)])
    identificator = pred(id, lambda x: x != ['module'], 'ID')
    disunction = lit(';') > constant("DIS")
    conjunction = lit(',') > constant("CON")
    dot = lit('.') > constant("DOT")
    lbr = lit('(')
    rbr = lit(')')
    tstile = lit(':-') > constant("TSTILE")

    # ---------------------------------------------------------------

    mod = module & identificator & dot

    # ---------------------------------------------------------------

    head = head_atom & tstile & expression & dot | head_atom & dot
    expression = M & disunction & expression | M
    M = P & conjunction & M | P
    P = lbr & expression & rbr | atom1
    atom = head_atom & dot
    atom1 = literal & atom2 | literal
    head_atom = identificator & atom2 | identificator
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


def parse_non_flag_or_prog(in_file_name):
    # print("here")
    out_file_name = in_file_name + ".out"  # output file
    file_in = open(in_file_name)  # open file
    s = str(file_in.read())  # read file
    i = 0
    prev_pos = 0
    mod_count = 0
    file_out = open(out_file_name, 'w')  # open output file
    while s[len(s) - 1] == ' ' or s[len(s) - 1] == '\n' or s[len(s) - 1] == '\t':
        s = s[:-1]
    while i < len(s):
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = str(PrologParser.mod.parse(current_expression))
        if result[:7] == "Success" and mod_count < 1:
            print_result(result, file_out)
            mod_count += 1
        else:
            result = str(PrologParser.head.parse(current_expression))
            if result[:7] == "Success":
                print_result(result, file_out)
            else:
                file_out.write("Syntax error!\n")
        prev_pos = i


def parse_atom(in_file_name):
    out_file_name = in_file_name + ".out"  # output file
    file_in = open(in_file_name)  # open file
    s = str(file_in.read())  # read file
    i = 0
    prev_pos = 0
    atom_count = 0
    file_out = open(out_file_name, 'w')  # open output file
    while s[len(s) - 1] == ' ' or s[len(s) - 1] == '\n' or s[len(s) - 1] == '\t':
        s = s[:-1]
    while i < len(s) and atom_count < 1:
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = str(PrologParser.atom.parse(current_expression))
        if result[:7] == "Success":
            print_result(result, file_out)
            atom_count += 1
        else:
            file_out.write("Syntax error!\n")
            atom_count += 1
        prev_pos = i


def parse_module(in_file_name):
    out_file_name = in_file_name + ".out"  # output file
    file_in = open(in_file_name)  # open file
    s = str(file_in.read())  # read file
    i = 0
    prev_pos = 0
    mod_count = 0
    file_out = open(out_file_name, 'w')  # open output file
    while s[len(s) - 1] == ' ' or s[len(s) - 1] == '\n' or s[len(s) - 1] == '\t':
        s = s[:-1]
    while i < len(s) and mod_count < 1:
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = str(PrologParser.mod.parse(current_expression))
        if result[:7] == "Success" and mod_count < 1:
            print_result(result, file_out)
            mod_count += 1
        else:
            file_out.write("Syntax error!\n")
            mod_count += 1
        prev_pos = i


def parse_relation(in_file_name):
    out_file_name = in_file_name + ".out"  # output file
    file_in = open(in_file_name)  # open file
    s = str(file_in.read())  # read file
    i = 0
    prev_pos = 0
    atom_count = 0
    file_out = open(out_file_name, 'w')  # open output file
    while s[len(s) - 1] == ' ' or s[len(s) - 1] == '\n' or s[len(s) - 1] == '\t':
        s = s[:-1]
    while i < len(s) and atom_count < 1:
        while i < len(s) and s[i] != '.':
            i += 1
        i += 1
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        current_expression = s[prev_pos:i]
        result = str(PrologParser.head.parse(current_expression))
        if result[:7] == "Success":
            print_result(result, file_out)
            atom_count += 1
        else:
            file_out.write("Syntax error!\n")
            atom_count += 1
        prev_pos = i


def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == "--prog":
            parse_non_flag_or_prog(sys.argv[2])
        elif sys.argv[1] == "--atom":
            parse_atom(sys.argv[2])
        elif sys.argv[1] == "--module":
            parse_module(sys.argv[2])
        elif sys.argv[1] == "--relation":
            parse_relation(sys.argv[2])
        else:
            print("Unknown flag\n")
    else:
        parse_non_flag_or_prog(sys.argv[1])


if __name__ == "__main__":
    main()
