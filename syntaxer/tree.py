class bc:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  WARNING = '\033[93m'
  ENDC = '\033[0m'
  UNDERLINE = '\033[4m'

def getMsgColor(value):
  if 'code' in value:
    return  bc.WARNING if value['code'] == 0 else bc.UNDERLINE
  return bc.HEADER

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
    # print value
    msgColor = getMsgColor(self.value)
    print '{}{} |>{}{}{}{}'.format(bc.OKBLUE, padding, bc.ENDC, msgColor, value['name'], bc.ENDC)
    for node in self.children:
      node.view(level + 1)
