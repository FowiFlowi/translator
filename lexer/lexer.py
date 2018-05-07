#!/usr/bin/python

import sys
import argparse

from handler import process
from pretty import out

def lexer(filename):
  with open(filename) as f:
    while True:
      result = process(f.read(1))
      if result != None:
        return result
        break

def printTokens(tokens):
  out(tokens)
