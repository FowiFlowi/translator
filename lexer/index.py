#!/usr/bin/python

import sys

from handler import process
from pretty import out

filename = sys.argv[1]

with open(filename) as f:
  while True:
    result = process(f.read(1))
    if result != None:
      # print result
      out(result['tokens'])
      break
