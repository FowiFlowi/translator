class bcolors:
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

class SemantyxerError(Exception):
  def __init__(self, value):
    self.value = value

class Semantyxer:
  def __init__(self, ast):
    self.labelNum = 0
    self.file = open('out.asm', 'w')
    try:
      self.processNode(ast)
    except SemantyxerError as e:
      token = e.value
      print ('{}ERROR:{} Wrong identifier \'{}{}{}\' on position {}{}, {}{}'
        .format(bcolors.FAIL, bcolors.ENDC, bcolors.BOLD, token['name'], bcolors.ENDC,
          bcolors.BOLD, token['line'], token['pos'], bcolors.ENDC))

  def processNode(self, node):
    nodeName = node.value['name']
    if nodeName == 'signal-program':       # <signal-program> --> <program>
      self.processSignalProgram(node)
    elif nodeName == 'program':            # <program> --> PROGRAM <procedure-identifier> ;
      self.processProgram(node)
    elif nodeName == 'block':              # <block> --> BEGIN <statements-list> END
      self.processBlock(node)
    elif nodeName == 'statementsList':     # <statements-list> --> <statement> <statementslist> | <empty>
      self.processStatementsList(node)
    elif nodeName == 'statement':          # <statement> --> <condition-statement> ENDIF ; |
      self.processStatement(node)          #  WHILE <conditional-expression> DO <statements-list> ENDWHILE;
    elif nodeName == 'conditionStatement': # <condition-statement> --> <incomplete-conditionstatement><alternative-part>
      self.processConditionStatement(node)

  def processSignalProgram(self, node):
    self.processNode(node.children[0]) 

  def processProgram(self, node):
    self.file.write('code SEGMENT\n\tASSUME cs:code\n')
    self.programName = node.children[1].children[0].value['name']
    self.processNode(node.children[3])

  def processBlock(self, node):
    self.file.write('begin:\n')
    self.processNode(node.children[1])
    self.file.write('\tret  0\n\tmov ax, 4c00h\n\tint 21h\ncode ENDS\n\tend begin\n')

  def processStatementsList(self, node):
    for child in node.children:
      self.processNode(child)

  def processStatement(self, node):
    if node.children[0].value['name'] == 'WHILE':
      firstLabel = '?L' + str(self.labelNum)
      self.file.write(firstLabel + ':\tNOP\n')
      self.labelNum += 1
      secondLabel = '?L' + str(self.labelNum)
      self.labelNum += 1
      command = self.processConditionalExpression(node.children[1])
      self.file.write('\t' + command + ' ' + secondLabel + '\n')
      self.processNode(node.children[3])
      self.file.write('\tJMP ' + firstLabel + '\n')
      self.file.write(secondLabel + ':\tNOP\n')
    else:
      self.processNode(node.children[0])

  def processConditionStatement(self, node):
    command = self.processConditionalExpression(node.children[0].children[1])
    firstLabel = '?L' + str(self.labelNum)
    self.labelNum += 1
    self.file.write('\t' + command + ' ' + firstLabel + '\n')
    secondLabel = '?L' + str(self.labelNum)
    self.labelNum += 1
    self.processNode(node.children[0].children[3])
    self.file.write('\tJMP ' + secondLabel + '\n')
    self.file.write(firstLabel + ':\tNOP\n')
    self.processNode(node.children[1])
    self.file.write(secondLabel + ':\tNOP\n')

  # <conditional-expression> --> <expression> <comparison-operator> <expression>
  def processConditionalExpression(self, node):
    childA = node.children[0].children[0].value
    childB = node.children[2].children[0].value
    a = childA['name']
    b = childB['name']
    if a == self.programName:
      raise SemantyxerError(childA)
    if b == self.programName:
      raise SemantyxerError(childB)

    comparison = node.children[1].children[0].value['name']
    self.file.write('\tMOV AX, ' + a + '\n')
    self.file.write('\tMOV BX, ' + b + '\n')
    self.file.write('\tCMP AX, BX\n')
    command = ''
    if comparison == '=':
      command = 'jne'
    elif comparison == '<>':
      command = 'je'
    elif comparison == '<=':
      command = 'ja'
    elif comparison == '<':
      command = 'jae'
    elif comparison == '>=':
      command = 'jb'
    elif comparison == '>':
      command = 'jbe'
    return command
