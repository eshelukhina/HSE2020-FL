import sys
import re

pos = 0
s = ''
sys_err = False
sys_err_string = "Correct relationship definition."


def parse_H(a):
    global pos
    global s
    global sys_err
    global sys_err_string
    err_L = parse_L(a)
    if err_L:
        sys_err_string = "No head. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
        sys_err = True
    if sys_err:
        return
    if s[pos] == ':' and s[pos + 1] == '-' and a[pos][1] == a[pos + 1][1] - 1:
        pos += 2
        if s[pos] == '.':
            sys_err_string = "No body. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
            sys_err = True
        if sys_err:
            return
        else:
            parse_E(a)
            if sys_err:
                return
    if s[pos] == '.':
        pos += 1
    else:
        sys_err_string = "Incorrect or extra symbol. Error in line " + str(a[pos][0]) + ", colon " + str(
            a[pos][1]) + "."
        sys_err = True
        if sys_err:
            return


def parse_L(a):
    global pos
    global s
    global sys_err
    global sys_err_string
    while re.match(r'[a-zA-Z_]+', s[pos]):
        pos += 1
    if re.match(r'[a-zA-Z_]+', s[pos - 1]):
        return False
    elif s[pos] != '(':
        sys_err = True
        sys_err_string = "Incorrect or extra symbol. Error in line " + str(a[pos][0]) + ", colon " + str(
            a[pos][1]) + "."
        return True
    elif s[pos] == '(':
        return True
    else:
        return True


def parse_B(parse_item, parse_sep, a):
    global s
    global sys_err
    global sys_err_string
    parse_item(a)
    if not parse_sep():
        if not re.match(r'[a-zA-Z_]+', s[pos]) and s[pos] != '(':
            if s[pos - 1] == ',':
                sys_err_string = "The conjunction has no right subexpression. Error in line " + str(
                    a[pos][0]) + ", colon " + str(a[pos][1]) + "."
                sys_err = True
                return
            if s[pos - 1] == ';' and s[pos] != '(':
                sys_err_string = "The disjunction has no right subexpression. Error in line " + str(
                    a[pos][0]) + ", colon " + str(a[pos][1]) + "."
                sys_err = True
                return
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
    global sys_err
    global sys_err_string
    if parse_L(a):
        if s[pos] == '(':
            pos += 1
        if sys_err:
            return
        parse_E(a)
        if s[pos] == ')':
            pos += 1
            if sys_err:
                return
        else:
            sys_err_string = "Unbalanced brackets. Error in line " + str(a[pos][0]) + ", colon " + str(a[pos][1]) + "."
            sys_err = True


def main():
    global s
    global sys_err_string
    global sys_err
    f = open(sys.argv[1])
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
        sys_err = True
        sys_err_string = "No point. Error in line " + str(a[n - 1][0]) + ", colon " + str(a[n - 1][1]) + "."
    else:
        while pos < n and not sys_err:
            parse_H(a)
    print(sys_err_string)


if __name__ == "__main__":
    main()
