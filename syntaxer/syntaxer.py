#!/usr/bin/python
import sys
# sys.path.append('../lexer')

# from lexer import lexer
from flow import program

def syntaxer(tokens):
  return program(tokens)

# syntaxer(lexer('../input')['tokens'])
# syntaxer(lexer(sys.argv[1])['tokens'])
