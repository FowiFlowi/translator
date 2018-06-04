class Syntaxer:
  def __init__(self, inputTokens):
    self.tokens = inputTokens
    self.comparisons = ['<=', '=', '<>', '>=', '>', '<']
    self.root = Node({'name': 'signal-program'})
    self.currNode = self.root
    self.currTokenIndx = 0
    self.error = False
    self.nT('program')

  def nT(self, funcName, branching = False): # nonTerminal
    parentNode = self.currNode
    func = getattr(self, funcName)
    self.addNode(func.__name__)
    result = func()
    self.currNode = parentNode
    return result if branching else self

  def nTB(self, funcName): # nonTerminal + branching
    return self.nT(funcName, True)

  def t(self, expected, raiseError = True, tokenField = 'name', expectedMsg = None): # terminal
    if self.currTokenIndx >= len(self.tokens):
      raise SyntaxerError('Unexpected end of file')

    token = self.tokens[self.currTokenIndx]
    token['terminal'] = True
    node = Node(token)
    self.currNode.add(node)
    self.currTokenIndx += 1

    value = token[tokenField]
    claim = False
    errorMsg = ''
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
    if not raiseError:
      return claim
    return self

  def program(self):
    try:
      self.t('PROGRAM').nT('procedureIdentifier').t(';').nT('block').t('.')
      if self.currTokenIndx != len(self.tokens):
        raise SyntaxerError('Unexpected extra code')
      return self.root
    except SyntaxerError as e:
      return self.errorHandler(e)

  def block(self):
    return self.t('BEGIN').nT('statementsList').t('END')

  def statementsList(self):
    return (True if self.nTB('statement') and self.nTB('statementsList') 
            else self.rollback().empty())

  def statement(self):
    if self.nTB('conditionStatement'):
      return self.t('ENDIF').t(';')

    if not self.rollback().t('WHILE', False):
      return False

    return self.nT('conditionalExpression').t('DO').nT('statementsList').t('ENDWHILE').t(';')

  def conditionStatement(self):
    return self.nTB('incompleteConditionStatement') and self.nTB('alternativePart')

  def incompleteConditionStatement(self):
    return self.t('IF', False) and self.nT('conditionalExpression').t('THEN').nT('statementsList')

  def alternativePart(self):
    if not self.t('ELSE', False):
      return self.rollback().empty()
    return self.nT('statementsList')

  def conditionalExpression(self):
    return self.nTB('expression') and self.nTB('comparisonOperator') and self.nTB('expression')

  def comparisonOperator(self):
    return self.t(self.comparisons)

  def expression(self):
    return self.t(lambda code: code >= 400 and code < 600, True, 'code', 'identifier or constant')

  def procedureIdentifier(self):
    return self.t(lambda code: code >= 400 and code < 500, True, 'code', 'procedure identifier')

  def empty(self):
    return self.addNode('<empty>')

  def rollback(self):
    self.currTokenIndx = self.currNode.value['indx']
    self.currNode.children = []
    return self

  def addNode(self, name, code = None):
    node = Node({'name': name, 'indx': self.currTokenIndx})
    self.currNode.add(node)
    if name == '<empty>':
      node.value['code'] = 0
      node.value['indx'] = None
    else:
      self.currNode = node
    return True

  def errorHandler(self, e):
    self.error = True
    if e.expected == None:
      print '{}ERROR:{} {}'.format(bc.FAIL, bc.ENDC, e.value)
    else:
      token = e.value
      print ('{}ERROR:{} Unexpected token \'{}{}{}\' on position {}{}, {}{}. Expected \'{}{}{}\''
        .format(bc.FAIL, bc.ENDC, bc.BOLD, token['name'], bc.ENDC,
          bc.BOLD, token['line'], token['pos'], bc.ENDC, bc.BOLD, e.expected, bc.ENDC))

class Node:
  def __init__(self, value):
    self.value = value
    self.children = []
    self.parent = None
  def add(self, node):
    assert isinstance(node, Node)
    node.parent = self
    self.children.append(node)
  def view(self, level = 0):
    padding = ''.join(' | ' for i in range(level))
    value = self.value
    msgColor = self.getMsgColor(self.value)
    print '{}{} |>{}{}{}{}'.format(bc.OKBLUE, padding, bc.ENDC, msgColor, value['name'], bc.ENDC)
    for node in self.children:
      node.view(level + 1)
  def getMsgColor(self, value):
    if 'code' in value:
      return  bc.WARNING if value['code'] == 0 else bc.UNDERLINE
    return bc.HEADER
    
class SyntaxerError(Exception):
  def __init__(self, value, expected = None):
    self.value = value
    self.expected = expected

class bc:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  WARNING = '\033[93m'
  ENDC = '\033[0m'
  UNDERLINE = '\033[4m'
  FAIL = '\033[91m'
  BOLD = '\033[1m'
