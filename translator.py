#!/usr/bin/python

import sys, getopt
sys.path.append('./lexer')

from lexer import lexer, printTokens
from syntaxer import Syntaxer
from semantyxer import Semantyxer

unixOptions = 'lsp:g'
gnuOptions = ['lexer', 'syntaxer', 'path', 'generator']
argumentList = sys.argv[1:]

try:
  path = None
  lexerPrint = False
  syntaxerPrint = False
  semantyxerPrint = False
  arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
  for arg, val in arguments:
    if arg in ['-p', '--path']:
      path = val
    elif arg in ['-l', '--lexer']:
      lexerPrint = True
    elif arg in ['-s', '--syntaxer']:
      syntaxerPrint = True
    elif arg in ['-g', '--generator']:
      semantyxerPrint = True

  if not path:
    raise getopt.error('path is required! (-p path)')

  tokens = lexer(path)['tokens']
  if lexerPrint:
    print 'TOKENS:'
    printTokens(tokens)

  syntaxer = Syntaxer(tokens)
  if syntaxerPrint:
    print 'AST:'
    syntaxer.root.view()

  if not syntaxer.error:
    Semantyxer(syntaxer.root)
    if semantyxerPrint:
      print 'ASM:'
      f = open('out.asm', 'r')
      print f.read()

except getopt.error as e:
  print str(e)
  sys.exit(2)

