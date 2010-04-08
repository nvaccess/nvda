#generate.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

"""Script to prepare an NVDA source tree for optimal execution.
This script:
* Generates Python code for COM interfaces to avoid doing this at runtime;
* Compiles source language files into binary form for use by NVDA;
* Generates the HTML documentation.
This should be run prior to executing NVDA from a clean source tree for the first time and before building a binary distribution with py2exe.
"""

#Bit of a dance to force comtypes generated interfaces in to our directory
import comtypes.client
comtypes.client.gen_dir='.\\comInterfaces'
import comtypes
import sys
sys.modules['comtypes.gen']=comtypes.gen=__import__("comInterfaces",globals(),locals(),[])

import os
from glob import glob
import txt2tags

COM_INTERFACES = (
	("UI Automation", comtypes.client.GetModule, "UIAutomationCore.dll"),
	("IAccessible 2", comtypes.client.GetModule, "typelibs/ia2.tlb"),
	("MS Active Accessibility", comtypes.client.GetModule, "oleacc.dll"),
	("Rich Edit library", comtypes.client.GetModule, "msftedit.dll"),
	("SAPI 5", comtypes.client.CreateObject, "Sapi.SPVoice"),
	("Acrobat Access", comtypes.client.GetModule, "typelibs/AcrobatAccess.tlb"),
	("Flash Accessibility", comtypes.client.GetModule, "typelibs/FlashAccessibility.tlb"),
)

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

	print "HTML documentation:"
	files = glob(r"..\user_docs\*\*.t2t")
	# Using txt2tags as a module to handle files is a bit weird.
	# It seems simplest to pretend we're running from the command line.
	txt2tags.exec_command_line(files)
	print

if __name__ == "__main__":
	main()
