"""Run SCons from the NVDA source environment.
"""

import sys
import os

sconsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "include", "scons", "src", "engine"))

if os.path.exists(sconsPath):
	sys.path.append(sconsPath)
	import SCons.Script
	SCons.Script.main()
else:
	raise OSError("Path %s does not exist. Perhaps try running git submodule update --init" % sconsPath)
