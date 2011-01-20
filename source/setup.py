#setup.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import gettext
gettext.install("nvda", unicode=True)
from distutils.core import setup
import py2exe as py2exeModule
from glob import glob
import fnmatch
from versionInfo import *
from py2exe import build_exe
import wx
import imp

MAIN_MANIFEST_EXTRA = r"""
<file name="brailleDisplayDrivers\handyTech\HtBrailleDriverServer.dll">
	<comClass
		description="HtBrailleDriver Class"
		clsid="{209445BA-92ED-4AB2-83EC-F24ACEE77EE0}"
		threadingModel="Apartment"
		progid="HtBrailleDriverServer.HtBrailleDriver"
		tlbid="{33257EFB-336F-4680-B94E-F5013BA6B9B3}" />
</file>
<file name="brailleDisplayDrivers\handyTech\HtBrailleDriverServer.tlb">
	<typelib tlbid="{33257EFB-336F-4680-B94E-F5013BA6B9B3}"
		version="1.0"
		helpdir="" />
</file>
<comInterfaceExternalProxyStub
	name="IHtBrailleDriverSink"
	iid="{EF551F82-1C7E-421F-963D-D9D03548785A}"
	proxyStubClsid32="{00020420-0000-0000-C000-000000000046}"
	baseInterface="{00000000-0000-0000-C000-000000000046}"
	tlbid="{33257EFB-336F-4680-B94E-F5013BA6B9B3}" />
<comInterfaceExternalProxyStub
	name="IHtBrailleDriver"
	iid="{43A71F9B-58EE-42D4-B58E-0F9FBA28D995}"
	proxyStubClsid32="{00020424-0000-0000-C000-000000000046}"
	baseInterface="{00000000-0000-0000-C000-000000000046}"
	tlbid="{33257EFB-336F-4680-B94E-F5013BA6B9B3}" />
"""

def getModuleExtention(thisModType):
	for ext,mode,modType in imp.get_suffixes():
		if modType==thisModType:
			return ext
	raise ValueError("unknown mod type %s"%thisModType)

# py2exe's idea of whether a dll is a system dll appears to be wrong sometimes, so monkey patch it.
origIsSystemDLL = build_exe.isSystemDLL
def isSystemDLL(pathname):
	dll = os.path.basename(pathname).lower()
	if dll in ("msvcp71.dll", "msvcp90.dll", "gdiplus.dll","mfc71.dll", "mfc90.dll"):
		# These dlls don't exist on many systems, so make sure they're included.
		return 0
	elif dll.startswith("api-ms-win-") or dll == "powrprof.dll":
		# These are definitely system dlls available on all systems and must be excluded.
		# Including them can cause serious problems when a binary build is run on a different version of Windows.
		return 1
	return origIsSystemDLL(pathname)
build_exe.isSystemDLL = isSystemDLL

class py2exe(build_exe.py2exe):
	"""Overridden py2exe command to:
		* Add a command line option --enable-uiAccess to enable uiAccess for the main executable
		* Add extra info to the manifest
		* Don't copy w9xpopen, as NVDA will never run on Win9x
	"""

	user_options = build_exe.py2exe.user_options + [
		("enable-uiAccess", "u", "enable uiAccess for the main executable"),
	]

	def initialize_options(self):
		build_exe.py2exe.initialize_options(self)
		self.enable_uiAccess = False

	def copy_w9xpopen(self, modules, dlls):
		pass

	def build_manifest(self, target, template):
		if target is self.distribution.windows[0]:
			# This is the main executable.
			isMainExec = True
			if self.enable_uiAccess:
				target.uac_info = (target.uac_info[0], True)
		else:
			isMainExec = False

		mfest, rid = build_exe.py2exe.build_manifest(self, target, template)

		if isMainExec:
			mfest = mfest[:mfest.rindex("</assembly>")]
			mfest += MAIN_MANIFEST_EXTRA + "</assembly>"

		return mfest, rid

def getLocaleDataFiles():
	NVDALocaleFiles=[(os.path.dirname(f), (f,)) for f in glob("locale/*/LC_MESSAGES/*.mo")]
	wxDir=wx.__path__[0]
	wxLocaleFiles=[(os.path.dirname(f)[len(wxDir)+1:], (f,)) for f in glob(wxDir+"/locale/*/LC_MESSAGES/*.mo")]
	return NVDALocaleFiles+wxLocaleFiles

def getRecursiveDataFiles(dest,source,excludes=()):
	rulesList=[]
	rulesList.append((dest,
		[f for f in glob("%s/*"%source) if not any(fnmatch.fnmatch(f,exclude) for exclude in excludes) and os.path.isfile(f)]))
	[rulesList.extend(getRecursiveDataFiles(os.path.join(dest,dirName),os.path.join(source,dirName),excludes=excludes)) for dirName in os.listdir(source) if os.path.isdir(os.path.join(source,dirName)) and not dirName.startswith('.')]
	return rulesList

compiledModExtention = getModuleExtention(imp.PY_COMPILED)
sourceModExtention = getModuleExtention(imp.PY_SOURCE)
setup(
	name = name,
	version=version,
	description=description,
	url=url,
	classifiers=[
'Development Status :: 3 - Alpha',
'Environment :: Win32 (MS Windows)',
'Topic :: Adaptive Technologies'
'Intended Audience :: Developers',
'Intended Audience :: End Users/Desktop',
'License :: OSI Approved :: GNU General Public License (GPL)',
'Natural Language :: English',
'Programming Language :: Python',
'Operating System :: Microsoft :: Windows',
],
	cmdclass={"py2exe": py2exe},
	windows=[
		{
			"script":"nvda.pyw",
			"uac_info": ("asInvoker", False),
			"icon_resources":[(1,"images/nvda.ico")],
			"version":"0.0.0.0",
			"description":"NVDA application",
			"product_version":version,
			"copyright":copyright,
		},
		{
			"script": "nvda_slave.pyw",
			"icon_resources": [(1,"images/nvda.ico")],
			"version": "0.0.0.0",
			"description": "NVDA slave",
			"product_version": version,
			"copyright": copyright,
		},
	],
	service=[{
		"modules": ["nvda_service"],
		"icon_resources": [(1, "images/nvda.ico")],
		"version": "0.0.0.0",
		"description": "NVDA service",
		"product_version": version,
		"copyright": copyright,
		"uac_info": ("requireAdministrator", False),
		"cmdline_style": "pywin32",
	}],
	options = {"py2exe": {
		"bundle_files": 3,
		"excludes": ["comInterfaces", "Tkinter"],
		"packages": ["NVDAObjects","virtualBuffers","appModules","brailleDisplayDrivers","synthDrivers"],
		# Can be removed once included by a bundled module.
		"includes": ["objbase"],
	}},
	data_files=[
		(".",glob("*.dll")+glob("*.manifest")+["builtin.dic"]),
		("documentation", ['../copying.txt', '../contributors.txt']),
		("lib", glob("lib/*.dll") + glob("lib/*.pdb")),
		("lib64", glob("lib64/*.dll") + glob("lib64/*.exe") + glob("lib64/*.pdb")),
		("comInterfaces", glob("comInterfaces/*%s"%compiledModExtention)),
		("waves", glob("waves/*.wav")),
		("images", glob("images/*.ico")),
		("louis/tables",glob("louis/tables/*"))
	] + (
		getLocaleDataFiles()
		+ getRecursiveDataFiles("synthDrivers", "synthDrivers", excludes=("*%s"%sourceModExtention,"*%s"%compiledModExtention))
		+ getRecursiveDataFiles("brailleDisplayDrivers", "brailleDisplayDrivers", excludes=("*%s"%sourceModExtention,"*%s"%compiledModExtention))
		+ getRecursiveDataFiles('documentation', '../user_docs', excludes=('*.t2t', '*.t2tconf'))
	),
)
