import sys
import re

pos = 0
s = ''


def parse_H(a):
    global pos
    global s
    err_L = parse_L()
    if err_L:
        s_err = "No head. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
        sys.exit(s_err)
    if s[pos] == ':' and s[pos + 1] == '-':
        pos += 2
        if s[pos] == '.':
            s_err = "No body. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
            sys.exit(s_err)
        else:
            parse_E(a)
    if s[pos] == '.':
        print("Correct relationship definition.")
        pos += 1
    else:
        s_err = "Something goes wrong. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
        sys.exit(s_err)


def parse_L():
    global pos
    global s
    if re.match(r'[a-z]+', s[pos]):
        pos += 1
        return False
    else:
        return True


def parse_B(parse_item, parse_sep, a):
    global s
    parse_item(a)
    if not parse_sep():
        if not re.match(r'[a-z]+', s[pos]):
            if s[pos - 1] == ',':
                s_err = "The conjunction has no right subexpression. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
                sys.exit(s_err)
            if s[pos - 1] == ';':
                s_err = "The disjunction has no right subexpression. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
                sys.exit(s_err)
        parse_B(parse_item, parse_sep, a)


def parse_E(a):
    global s
    parse_B(parse_M, parse_plus, a)


def parse_plus():
    global pos
    global s
    if s[pos] == ';':
        pos += 1
        return False
    else:
        return True


def parse_M(a):
    parse_B(parse_P, parse_mul, a)


def parse_mul():
    global s
    global pos
    if s[pos] == ',':
        pos += 1
        return False
    else:
        return True


def parse_P(a):
    global s
    global pos
    if parse_L():
        if s[pos] == '(':
            pos += 1
        parse_E(a)
        if s[pos] == ')':
            pos += 1
        else:
            s_err = "Unbalanced brackets. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
            sys.exit(s_err)


def main():
    global s
    f = open('text.txt')
    s = str(f.read())
    ss = s
    k = 0
    s = s.replace(' ', '')
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    i = 0
    str_num = 1
    char_num_in_str = 0
    a = [0 for j in range(len(s))]
    while i < len(ss) and k < len(s):
        if ss[i] == s[k]:
            a[k] = (str_num, char_num_in_str)
            k += 1
            i += 1
            char_num_in_str += 1
        elif ss[i] == '\n':
            str_num += 1
            char_num_in_str = 0
            i += 1
        else:
            i += 1
            char_num_in_str += 1
    n = len(s)
    if s[n - 1] != '.':
        sys.exit("No point.")
    while pos < n:
        parse_H(a)


if __name__ == "__main__":
    main()

