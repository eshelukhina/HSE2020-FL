# Синтаксический анализатор с использованием генератора парсеров из семейства yacc для упрощенного подмножества пролога
### Грамматика
```
- H  -> A1. | A1  :- E.        H  -  head
- E  -> (M + E) | M            E  - expression
- M  -> (P * M) | P            M  - disjunction
- P  -> A1 | (E)               P  - conjunction
- A1 -> L A2 | L               A1 - atom1
- A2 -> A1 | (A3) | (A3) A2    A2 - atom2
- A3 -> A1 | (A3)              A3 - atom3, L - literal
```
### Сборка
```
  python3 parse.py test.txt
```
### Содержание выходного файла
```
Ex, TSTILE, f, PLUS, k, DOT
Syntax error
HSE, TSTILE, a, PLUS, LBR, a, RBR, DOT
Syntax error
Syntax error
Ex, TSTILE, a, PLUS, LBR, b, MULT, c, d, MULT, e, RBR, DOT
HelloWorld, DOT
f, TSTILE, LBR, LBR, k, RBR, PLUS, c, RBR, MULT, d, MULT, LBR, f, MULT, a, RBR, DOT
Function, TSTILE, qwerty, MULT, qwerty, PLUS, qwerty, MULT, qwerty, DOT
Syntax error

```
