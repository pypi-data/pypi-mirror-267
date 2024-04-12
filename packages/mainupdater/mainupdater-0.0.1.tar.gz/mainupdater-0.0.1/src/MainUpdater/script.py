from MainUpdater.main import *
from sys import argv
def updateAll():
  if len(argv)==1:
    update_all(os.getcwd(),cli=True)
  else:
    for i in argv[1:]:
      update_all(i,cli=True)