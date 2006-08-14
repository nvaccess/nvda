import sys
import debug
from constants import *


characterSymbols=None
roleNames=None
stateNames=None
textSymbols=None

def load(label):
	f=open("dictionaries\%s.py"%label)
	if f is None:
		debug.writeError("dictionaries.load: could not open dictionaries\%s.py"%label)
		system.exit()
	try:
		globals()[label]=eval(f.read())
	except:
		debug.writeException("dictionaries.load: exception loading %s data"%label)
		sys.exit()

