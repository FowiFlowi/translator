from tree import Node
from utils import errorHandler

comparisons = ['<=', '=', '<>', '>=', '>', '<']

root = Node({'name': 'signal-program'})
currNode = root
currTokenIndx = 0

class SyntaxerError(Exception):
  def __init__(self, value, expected = None):
    self.value = value
    self.expected = expected

def nonTerminal(nonTerminalFunc):
  def wrapper(inputTokens = None):
    global currNode
    if inputTokens:
      global tokens
      tokens = inputTokens
    parentNode = currNode
    addNode(nonTerminalFunc.__name__)
    result = nonTerminalFunc()
    currNode = parentNode
    return result
  return wrapper

def terminal(expected, raiseError = True, tokenField = 'name', expectedMsg = None):
  global currTokenIndx
  if currTokenIndx >= len(tokens):
    raise SyntaxerError('Unexpected end of file')

  token = tokens[currTokenIndx]
  token['terminal'] = True
  node = Node(token)
  currNode.add(node)
  currTokenIndx += 1

  value = token[tokenField]
  claim = False
  errorMsg = 'valid'
  if isinstance(expected, list):
    claim = value in expected
    errorMsg = 'one of them: '+', '.join(expected)
  elif callable(expected):
    claim = expected(value)
    errorMsg = expectedMsg
  else:
    claim = value == expected
    errorMsg = expected

  if not claim and raiseError:
    raise SyntaxerError(token, errorMsg)
  return claim

def rollback():
  global currTokenIndx
  currTokenIndx = currNode.value['indx']
  currNode.children = []

def addNode(name, code = None):
  global currNode
  node = Node({'name': name, 'indx': currTokenIndx})
  currNode.add(node)
  if name == '<empty>':
    node.value['code'] = 0
    node.value['indx'] = None
  else:
    currNode = node
  return True

@nonTerminal
def program():
  try:
    terminal('PROGRAM')
    procedureIdentifier()
    terminal(';')
    block()
    terminal('.')

    if currTokenIndx != len(tokens):
      raise SyntaxerError('Unexpected extra code')
    return root
  except SyntaxerError as e:
    return errorHandler(e, root)

@nonTerminal
def block():
  terminal('BEGIN')
  statementsList()
  return terminal('END')

@nonTerminal
def statementsList():
  if not statement() or not statementsList():
    rollback()
    return addNode('<empty>')
  return True
  
@nonTerminal
def statement():
  if conditionStatement():
    terminal('ENDIF')
    return terminal(';')

  rollback()
  if not terminal('WHILE', False):
    return False

  conditionalExpression()
  terminal('DO')
  statementsList()
  terminal('ENDWHILE')
  return terminal(';')

@nonTerminal
def conditionStatement():
  return incompleteConditionStatement() and alternativePart()

@nonTerminal
def incompleteConditionStatement():
  if not terminal('IF', False):
    return False

  conditionalExpression()
  terminal('THEN')
  return statementsList()

@nonTerminal
def alternativePart():
  if not terminal('ELSE', False):
    rollback()
    return addNode('<empty>')
  return statementsList()

@nonTerminal
def conditionalExpression():
  return expression() and comparisonOperator() and expression()

@nonTerminal
def comparisonOperator():
  return terminal(comparisons)

@nonTerminal
def expression():
  return terminal(lambda code: code >= 400 and code < 600, True, 'code', 'identifier or constant')

@nonTerminal
def procedureIdentifier():
  return terminal(lambda code: code >= 400 and code < 500, True, 'code', 'procedure identifier')
