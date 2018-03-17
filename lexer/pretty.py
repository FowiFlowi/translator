class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def out(input):
  print bcolors.HEADER, 'line  pos  code  name\n----------------------', bcolors.ENDC
  for token in input:
    print '{:4} {:4} {}{:5}{}  {}{}{}'.format(token['line'], token['pos'], bcolors.OKBLUE, token['code'], bcolors.ENDC, bcolors.BOLD, token['name'], bcolors.ENDC)