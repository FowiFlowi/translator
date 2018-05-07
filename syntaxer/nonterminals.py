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

def nonTerminal(terminalFunc):
  def wrapper():
    global currNode
    parentNode = currNode
    addNode(terminalFunc.__name__)
    result = terminalFunc()
    currNode = parentNode
    return result
  return wrapper

def getToken():
  global currTokenIndx
  if currTokenIndx >= len(tokens):
    raise SyntaxerError('Unexpected end of file')

  token = tokens[currTokenIndx]
  token['terminal'] = True
  node = Node(token)
  currNode.add(node)

  currTokenIndx += 1
  return token

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

def program(inputTokens):
  global tokens
  tokens = inputTokens
  addNode('program')

  if (len(tokens) < 3):
    raise SyntaxerError('Unexpected end of file')
  try:
    token = getToken()
    if token['name'] != 'PROGRAM':
      raise SyntaxerError(token, 'PROGRAM')

    procedureIdentifier()
    token = getToken()
    if token['code'] != 59: # ;
      raise SyntaxerError(token, ';')

    block()
    token = getToken()
    if token['code'] != 46: # .
      raise SyntaxerError(token, '.')

    if currTokenIndx != len(tokens):
      raise SyntaxerError('Unexpected extra code')

    return root
  except SyntaxerError as e:
    if e.expected == None:
      print '{}ERROR:{} {}'.format(bcolors.FAIL, bcolors.ENDC, e.value)
    else:
      token = e.value
      print ('{}ERROR:{} Unexpected token \'{}{}{}\' on position {}{}, {}{}. Expected \'{}{}{}\''
        .format(bcolors.FAIL, bcolors.ENDC, bcolors.BOLD, token['name'], bcolors.ENDC,
          bcolors.BOLD, token['line'], token['pos'], bcolors.ENDC, bcolors.BOLD, e.expected, bcolors.ENDC))
      return root

@nonTerminal
def block():
  token = getToken()
  if token['name'] != 'BEGIN':
    raise SyntaxerError(token, 'BEGIN')

  statementsList()
  token = getToken()
  if token['name'] != 'END':
    raise SyntaxerError(token, 'END')

  return True

@nonTerminal
def statementsList():
  if not statement() or not statementsList():
    rollback(currNode)
    return addNode('<empty>')
  return True
  

@nonTerminal
def statement():
  if conditionStatement():
    token = getToken()
    if token['name'] != 'ENDIF':
      raise SyntaxerError(token, 'ENDIF')

    token = getToken()
    if token['code'] != 59: # ;
      raise SyntaxerError(token, ';')

    return True

  rollback(currNode)
  token = getToken()
  if token['name'] != 'WHILE':
    return False

  conditionalExpression()
  token = getToken()
  if token['name'] != 'DO':
    raise SyntaxerError(token, 'DO')

  statementsList()
  token = getToken()
  if token['name'] != 'ENDWHILE':
    raise SyntaxerError(token, 'ENDWHILE')

  token = getToken()
  if token['code'] != 59: # ;
    raise SyntaxerError(token, ';')

  return True

@nonTerminal
def conditionStatement():
  return incompleteConditionStatement() and alternativePart()

@nonTerminal
def incompleteConditionStatement():
  if getToken()['name'] != 'IF':
    return False

  conditionalExpression()
  token = getToken()
  if token['name'] != 'THEN':
    raise SyntaxerError(token, 'THEN')

  return statementsList()

@nonTerminal
def alternativePart():
  if getToken()['name'] != 'ELSE':
    rollback(currNode)
    return addNode('<empty>')
  return statementsList()

@nonTerminal
def conditionalExpression():
  return expression() and comparisonOperator() and expression()

@nonTerminal
def comparisonOperator():
  token = getToken()
  if token['name'] not in comparisons:
    raise SyntaxerError(token, 'one of them: ' + ', '.join(comparisons))
  return True

@nonTerminal
def expression():
  token = getToken()
  code = token['code']
  if code < 400 or code >= 600:
    raise SyntaxerError(token, 'identifier or constant')
  return True

@nonTerminal
def procedureIdentifier():
  token = getToken()
  code = token['code']
  if code < 400 or code >= 500:
    raise SyntaxerError(token, 'identifier')
  return True
