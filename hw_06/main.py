from parsita import *
from collections import namedtuple
from parsita.util import constant
from parsita.util import splat


class PrologParser(TextParsers, whitespace='[ \t\n]*'):
    literal = reg(r'[A-Za-z_][A-Za-z_0-9]*') > (lambda x: ["Atom", str(x)])
    disunction = lit(';') > constant("DIS")
    conjunction = lit(',') > constant("CON")
    dot = lit('.') > constant("DOT")
    lbr = lit('(')
    rbr = lit(')')
    tstile = lit(':-') > constant("TSTILE")
    # ---------------------------------------------------------------
    head = atom1 & tstile & expression & dot | atom1 & dot
    expression = M & disunction & expression | M
    M = P & conjunction & M | P
    P = lbr & expression & rbr | atom1
    atom1 = literal & atom2 | literal
    atom2 = lbr & atom3 & rbr & atom2 | atom1 | lbr & atom3 & rbr
    atom3 = atom1 | lbr & atom3 & rbr
    # ----------------------------------------------------------------


def main():
    strings = [
        "f (cons h t) :- g h, f t."
    ]

    for string in strings:
        result = str(PrologParser.head.parse(string))
        result = result.replace(')', '')
        result = result.replace('(', '')
        result = result.replace('\'', '')
        result = result.replace(',', '')
        result = result.replace('[', '(')
        result = result.replace(']', ')')
        result = result.replace('"', '')
        if result[:7] == "Success":
            print(result[8:len(result) - 1])
        else:
            print("Syntax error!")


if __name__ == "__main__":
    main()
