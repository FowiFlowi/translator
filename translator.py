#!/usr/bin/python

import sys, getopt
sys.path.append('./lexer')
sys.path.append('./syntaxer')

from lexer import lexer, printTokens
from syntaxer import syntaxer
unixOptions = 'lsp:'
gnuOptions = ['lexer', 'syntaxer', 'path']
argumentList = sys.argv[1:]

try:
    path = None
    lexerPrint = False
    syntaxerPrint = False
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    for arg, val in arguments:
      if arg in ['-p', '--path']:
        path = val
      elif arg in ['-l', '--lexer']:
        lexerPrint = True
      elif arg in ['-s', '--syntaxer']:
        syntaxerPrint = True
    
    if not path:
      raise getopt.error('path is required! (-p path)')

    tokens = lexer(path)['tokens']
    if lexerPrint:
      printTokens(tokens)
    rootAST = syntaxer(tokens)
    if syntaxerPrint:
      rootAST.view()

except getopt.error as e:
    print str(e)
    sys.exit(2)

