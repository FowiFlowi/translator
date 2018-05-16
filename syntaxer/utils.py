class bcolors:
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

def errorHandler(e, root):
  if e.expected == None:
    print '{}ERROR:{} {}'.format(bcolors.FAIL, bcolors.ENDC, e.value)
  else:
    token = e.value
    print ('{}ERROR:{} Unexpected token \'{}{}{}\' on position {}{}, {}{}. Expected \'{}{}{}\''
      .format(bcolors.FAIL, bcolors.ENDC, bcolors.BOLD, token['name'], bcolors.ENDC,
        bcolors.BOLD, token['line'], token['pos'], bcolors.ENDC, bcolors.BOLD, e.expected, bcolors.ENDC))
  return root

