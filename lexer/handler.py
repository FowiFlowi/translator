import json
import os

from process_state import process_num, process_idn, process_dm, process_mdm

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

with open(os.path.dirname(os.path.realpath(__file__)) + '/dictionary.json', 'r') as f:
  dic = json.load(f)

currPos = 1
currLine = 1
state = 'S'
delimeters = []
m_delimeters = []
tokens = []
idns = []
consts = []

def process(c):
  global currPos
  global currLine
  global state
  
  ac = None if not c else ord(c) # char in ascii

  if state == 'WS' and ac not in dic['spaces']:
    state = 'S'
  elif state == 'R' and (ac in dic['spaces'] or c in dic['delimeters'] or not c):
    state = 'S'

  elif state == 'NUM':
    result = process_num(c)
    if result == False:
      outError('Wrong symbol defining number: ', c)
      state = 'R'
    elif result != None:
      processToken(result, state)
      state = 'S'

  elif state == 'IDN':
    result = process_idn(c)
    if result == False:
      outError('Wrong symbol defining identifier: ', c)
      state = 'R'
    elif result != None:
      processToken(result, state)
      state = 'S'

  elif state == 'MDM':
    result = process_mdm(c)
    if result != None:
      processToken(result, state)
      state = 'S'

  elif state == 'BCOM':
    if c != '*':
      outError('Expected \'*\' instead of', c)
      state = 'S'
    else:
      state = 'COM'

  elif state == 'COM':
    if not c:
      outError('Unexpected end of file', c)
      state = 'S'
    elif c == '*':
      state = 'ECOM'

  elif state == 'ECOM':
    if not c:
      outError('Unexpected end of file', c)
      state = 'S'
    elif c == ')':
      state = 'S'
      currPos += 1
      return None
    elif c == '*':
      state = 'ECOM'
    else:
      state = 'COM'


  # handle start state
  if state == 'S':
    if not c:
      return {
        'consts': consts,
        'idns': idns,
        'tokens': tokens,
        'delimeters': delimeters,
        'm_delimeters': m_delimeters
      }

    elif c in dic['delimeters']:
      result = process_dm(c)
      if result != None:
        currPos += 1
        processToken(result, 'DM')
        currPos -= 1
        state = 'S'
      else:
        state = 'MDM'
    elif c == '(':
      state = 'BCOM'
    elif ac in dic['spaces']:
      state = 'WS'
    elif c.isdigit():
      state = 'NUM'
      process_num(c)
    elif c.isalpha():
      state = 'IDN'
      process_idn(c)
    else:
      outError('Illegal symbol', c)


  # if ac in dic['spaces']:
    # out('<s>', ac)
  if ac == 10 or ac == 13:
    currPos = 0
    currLine += 1
  # else:
  #   out(c, ac)

  currPos += 1
  return None

def processToken(token, type):
  code = None

  if type == 'IDN':
    for i, word in enumerate(dic['reserved']):
      if word == token.upper():
        code = 300 + i
        break
    if code == None:
      code = putToken(idns, token, 400)
  elif type == 'NUM':
    code = putToken(consts, token, 500)
  elif type == 'DM':
    code = putToken(delimeters, token)
  elif type == 'MDM':
    code = putToken(m_delimeters, token, 300)

  tokens.append({ 'name': token, 'line': currLine, 'pos': currPos - len(token), 'code': code })


def putToken(table, token, indx = None):
  code = None

  for i, word in enumerate(table):
    if word['name'] == token:
      code = indx + i + 1 if indx else ord(token)
      break
  if code == None:
    code = indx + len(table) + 1 if indx else ord(token)
    table.append({ 'name': token, 'code': code })

  return code

def out(c, ascii):
  print currLine, currPos, c, ascii

def outError(msg, c):
  print '{}ERROR:{} {} \'{}\' on position {}{}, {}{}'.format(bcolors.FAIL, bcolors.ENDC, msg, c, bcolors.BOLD, currLine, currPos, bcolors.ENDC)