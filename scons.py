"""Run SCons from the NVDA source environment.
"""

import sys
import os

sconsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "include", "scons"))

if os.path.exists(sconsPath):
	# sys.path[0] will always be the current dir, which should take precedence.
	# Insert path to the SCons folder after that.
	sys.path[1:1] = (sconsPath,)
	import SCons.Script
	SCons.Script.Main.main()
else:
	raise OSError("Path %s does not exist. Perhaps try running git submodule update --init" % sconsPath)
