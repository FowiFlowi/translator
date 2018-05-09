from tree import Node

comparisons = ['<=', '=', '<>', '>=', '>', '<']

root = Node({'name': 'signal-program'})
currNode = root
currTokenIndx = 0

class bcolors:
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

class SyntaxerError(Exception):
  def __init__(self, value, expected = None):
    self.value = value
    self.expected = expected

def errorHandler(e):
  if e.expected == None:
    print '{}ERROR:{} {}'.format(bcolors.FAIL, bcolors.ENDC, e.value)
  else:
    token = e.value
    print ('{}ERROR:{} Unexpected token \'{}{}{}\' on position {}{}, {}{}. Expected \'{}{}{}\''
      .format(bcolors.FAIL, bcolors.ENDC, bcolors.BOLD, token['name'], bcolors.ENDC,
        bcolors.BOLD, token['line'], token['pos'], bcolors.ENDC, bcolors.BOLD, e.expected, bcolors.ENDC))
  return root

def nonTerminal(nonTerminalFunc):
  def wrapper(inputTokens = None):
    if inputTokens:
      global tokens
      tokens = inputTokens
    global currNode
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
  if isinstance(expected, list):
    claim = expected if callable(expected) else value in expected
    if not claim and raiseError:
      raise SyntaxerError(token, 'one of them: ' + ', '.join(expectedMsg if expectedMsg else expected))
    else:
      return claim
  else:
    claim = expected if callable(expected) else value == expected
    if not claim and raiseError:
      raise SyntaxerError(token, expectedMsg if expectedMsg else expected)
    else:
      return claim

def rollback(node):
  global currTokenIndx
  global currNode
  currTokenIndx = node.value['indx']
  node.children = []
  currNode = node

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
    return errorHandler(e)

@nonTerminal
def block():
  terminal('BEGIN')
  statementsList()
  return terminal('END')

@nonTerminal
def statementsList():
  if not statement() or not statementsList():
    rollback(currNode)
    return addNode('<empty>')
  return True
  
@nonTerminal
def statement():
  if conditionStatement():
    terminal('ENDIF')
    return terminal(';')

  rollback(currNode)
  if terminal('WHILE', False) == False:
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
  if terminal('IF', False) == False:
    return False

  conditionalExpression()
  terminal('THEN')
  return statementsList()

@nonTerminal
def alternativePart():
  if terminal('ELSE', False) == False:
    rollback(currNode)
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
  return terminal(lambda code: code >= 400 and code < 500, True, 'code', 'identifier')
