"""Run SCons from the NVDA source environment.
"""

import sys
import os
import platform
# Variables for storing required version of Python, and the version which is used to run this script.
requiredPythonMajor ="2"
requiredPythonMinor = "7"
requiredPythonArchitecture = "32bit"
installedPythonMajor = sys.version_info.major
installedPythonMinor = sys.version_info.minor
installedPythonArchitecture = platform.architecture()[0]
# Ensure, that we are running with Python 2.7 32-bit, otherwise inform the user and exit.
if installedPythonArchitecture != requiredPythonArchitecture and installedPythonMajor != requiredPythonMajor and installedPythonMinor != requiredPythonMinor:
	print "This script is started with Python "+str(installedPythonMajor)+"."+str(installedPythonMinor)+" "+installedPythonArchitecture+", however to build NVDA you have to use Python", str(requiredPythonMajor)+"."+str(requiredPythonMinor), requiredPythonArchitecture+"."
	print "Please install the needed version of Python and launch SCons again, or if you have mulltiple versions of Python installed start this script with required version explicitly."
	sys.exit()
else:
	sys.path.append(os.path.abspath(
		os.path.join(__file__, "..", "source")))
	import sourceEnv
	del sys.path[-1]
	import SCons.Script
	SCons.Script.main()
