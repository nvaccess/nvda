#generate.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Script to prepare an NVDA source tree for optimal execution.
This script:
* Generates Python code for COM interfaces to avoid doing this at runtime;
* Compiles source language files into binary form for use by NVDA;
* Compiles appModules and synthDrivers into Python byte code to eliminate the need to do this on launch.
This should be run prior to executing NVDA from a clean source tree for the first time and before building a binary distribution with py2exe.
"""

#Force comtypes generated COM interfaces in to a local module
import comtypes_gen 
comtypes_gen.setAsComtypesGenModule()

import os
import sys
from glob import glob
import comtypes.client
import compileall

COM_INTERFACES = (
	("MS HTML", comtypes.client.GetModule, "mshtml.tlb"),
	("IAccessible 2", comtypes.client.GetModule, "lib/ia2.tlb"),
	("IService Provider library", comtypes.client.GetModule, "lib/servprov.tlb"),
	("MS Active Accessibility", comtypes.client.GetModule, "oleacc.dll"),
	("SAPI 5", comtypes.client.CreateObject, "Sapi.SPVoice"),
	("SAPI 4", comtypes.client.CreateObject, "ActiveVoice.ActiveVoice"),
)
COMPILE_DIRS = ("appModules", "synthDrivers")

def main():
	print "COM interfaces:"
	for desc, func, interface in COM_INTERFACES:
		print "%s:" % desc,
		try:
			func(interface)
			print "done."
		except:
			print "not found."
	print

	print "Language files:"
	poFiles=glob('locale/*/LC_MESSAGES/nvda.po')
	for f in poFiles:
		print f
		os.spawnv(os.P_WAIT,r"%s\python.exe"%sys.exec_prefix,['python',r'"%s\Tools\i18n\msgfmt.py"'%sys.exec_prefix,f])
	print

	print "Byte code compilation:"
	for dir in COMPILE_DIRS:
		compileall.compile_dir(dir, maxlevels=0)

if __name__ == "__main__":
	main()
