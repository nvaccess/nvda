#generate.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

"""Script to prepare an NVDA source tree for optimal execution.
This script:
* Generates Python code for COM interfaces to avoid doing this at runtime;
This should be run prior to executing NVDA from a clean source tree for the first time and before building a binary distribution with py2exe.
"""

#Bit of a dance to force comtypes generated interfaces in to our directory
import comtypes.client
comtypes.client.gen_dir='.\\comInterfaces'
import sys
sys.modules['comtypes.gen']=comtypes.gen=__import__("comInterfaces",globals(),locals(),[])

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

if __name__ == "__main__":
	main()
