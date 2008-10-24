#setup.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import gettext
gettext.install("nvda", unicode=True)
from distutils.core import setup
import py2exe
from glob import glob
from versionInfo import *
from py2exe import build_exe
import wx

# py2exe insists on excluding certain dlls that don't seem to exist on many systems, so hackishly force them to be included.
origIsSystemDLL = build_exe.isSystemDLL
def isSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ("msvcp71.dll", "gdiplus.dll","mfc71.dll"):
		return 0
	return origIsSystemDLL(pathname)
build_exe.isSystemDLL = isSystemDLL

def getLocaleDataFiles():
	NVDALocaleFiles=[(os.path.dirname(f), (f,)) for f in glob("locale/*/LC_MESSAGES/*.mo")]
	wxDir=wx.__path__[0]
	wxLocaleFiles=[(os.path.dirname(f)[len(wxDir)+1:], (f,)) for f in glob(wxDir+"/locale/*/LC_MESSAGES/*.mo")]
	return NVDALocaleFiles+wxLocaleFiles

def getRecursiveDataFiles(dest,source):
	rulesList=[]
	rulesList.append((dest,filter(os.path.isfile,glob("%s/*"%source))))
	[rulesList.extend(getRecursiveDataFiles(os.path.join(dest,dirName),os.path.join(source,dirName))) for dirName in os.listdir(source) if os.path.isdir(os.path.join(source,dirName)) and not dirName.startswith('.')]
	return rulesList

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
	windows = [{
		"script":"nvda.pyw",
		"icon_resources":[(1,"images/nvda.ico")],
	}],
	options = {"py2exe": {
		"bundle_files": 3,
		"excludes": ["comInterfaces"],
		"packages": ["NVDAObjects","virtualBuffers_old","virtualBuffers"],
		# The explicit inclusion of ui can be removed once ui is imported by a bundled module.
		# The explicit inclusion of brlapi is required because it is only imported by the brltty display driver, which is not a bundled module.
		"includes": ["ui", "brlapi"],
	}},
	zipfile = None,
	data_files=[
		(".",glob("*.dll")),
		("documentation", ['../copying.txt', '../contributors.txt']),
		("comInterfaces", glob("comInterfaces/*.pyc")),
		("appModules", glob("appModules/*.py*")),
		("appModules", glob("appModules/*.kbd")),
		("lib", glob("lib/*")),
		("waves", glob("waves/*.wav")),
		("images", glob("images/*.ico")),
		("speechdicts", glob("speechdicts/*.dic")),
		("louis/tables",glob("louis/tables/*"))
	] + getLocaleDataFiles()+getRecursiveDataFiles('documentation','../user_docs')+getRecursiveDataFiles('synthDrivers','synthDrivers')+getRecursiveDataFiles('brailleDisplayDrivers','brailleDisplayDrivers'),
)
