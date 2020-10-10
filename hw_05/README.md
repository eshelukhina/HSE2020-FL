# Синтаксический анализатор с использованием генератора парсеров из семейства yacc для упрощенного подмножества пролога
### Грамматика
```
- H  -> A1. | A1  :- E.        H  -  head
- E  -> (M + E) | M            E  - expression
- M  -> (P * M) | P            M  - disjunction
- P  -> A1 | (E)               P  - conjunction
- A1 -> L A2 | L               A1 - atom1
- A2 -> A1 | (A3) | (A3) A2    A2 - atom2
- A3 -> L A2                   A3 - atom3, L - literal
```
### Сборка
```
  python3 parse.py "test_file_name"
```
