# Translator
Translator from university course of program engineering.
Created on python.

Grammar
```text
1. <signal-program> --> <program>
2. <program> --> PROGRAM <procedure-identifier> ;
  <block>.
3. <block> --> BEGIN <statements-list> END
4. <statements-list> --> <statement> <statementslist> | <empty>
5. <statement> --> <condition-statement> ENDIF ; |
  WHILE <conditional-expression> DO
  <statements-list> ENDWHILE ;
6. <condition-statement> --> <incomplete-conditionstatement><alternative-part>
7. <incomplete-condition-statement> --> IF <conditional-expression> THEN <statementslist>
8. <alternative-part> --> ELSE <statements-list> | <empty>
9. <conditional-expression> --> <expression> <comparison-operator> <expression>
10. <comparison-operator> --> <= | = | <> | >= | > | <
11. <expression> --> <variable-identifier> | <unsigned-integer>
12. <variable-identifier> --> <identifier>
13. <procedure-identifier> --> <identifier>
14. <identifier> --> <letter><string>
15. <string> --> <letter><string> | <digit><string> | <empty>
16. <unsigned-integer> --> <digit><digits-string>
17. <digits-string> --> <digit><digits-string> | <empty>
18. <digit> --> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
19. <letter> --> A | B | C | D | ... | Z
```

## Stages
- [Lexical analyzer](#lexer)

## lexer
Produces tokens and checks for the lexical errors.

Input
![input](https://i.imgur.com/qtDvj3c.png)

Output
![output](https://i.imgur.com/DraxFZI.png)