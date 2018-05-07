import json
import os

mdm_token = ''
idn_token = ''
num_token = ''

with open(os.path.dirname(os.path.realpath(__file__)) + '/dictionary.json', 'r') as f:
  dic = json.load(f)

def process_dm(c):
  global mdm_token

  if c == '<' or c == '>':
    mdm_token += c
  else:
    return c

  return None

def process_mdm(c):
  global mdm_token

  if len(mdm_token) == 1 and (c == '=' or c == '>'):
    mdm_token += c
  else:
    result = mdm_token
    mdm_token = ''
    return result

  return None

def process_idn(c):
  global idn_token

  ac = None if not c else ord(c)

  if c.isalpha() or c.isdigit():
    idn_token += c
  elif c in dic['delimeters'] or ac in dic['spaces'] or not c:
    result = idn_token
    idn_token = ''
    return result
  else:
    idn_token = ''
    return False

  return None

def process_num(c):
  global num_token

  ac = None if not c else ord(c)

  if c.isdigit():
    num_token += c
  elif c in dic['delimeters'] or ac in dic['spaces'] or not c:
    result = num_token
    num_token = ''
    return result
  else:
    num_token = ''
    return False
    
  return None
