#setup.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
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

# py2exe insists on excluding certain dlls that don't seem to exist on many systems, so hackishly force them to be included.
origIsSystemDLL = build_exe.isSystemDLL
def isSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ("msvcp71.dll", "gdiplus.dll","mfc71.dll"):
		return 0
	return origIsSystemDLL(pathname)
build_exe.isSystemDLL = isSystemDLL

def getLocaleDataFiles():
	return [(os.path.dirname(f), (f,)) for f in glob("locale/*/LC_MESSAGES/*.mo")]

def getUserDocsDataFiles():
	docs=[(os.path.dirname(f).replace("../user_docs","documentation"), (f,)) for f in glob("../user_docs/*/*.txt")]
	docs.append(('documentation',glob('../user_docs/*.txt')))
	return docs

setup(
	name = name,
	version=version,
	description=description,
	maintainer=maintainer,
	maintainer_email=maintainer_email,
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
	windows = ["nvda.pyw"],
	options = {"py2exe": {"bundle_files": 3}},
	zipfile = None,
	data_files = [
		("documentation", ['../copying.txt','../todo.txt','../bugs.txt']), 
		("comInterfaces", glob("comInterfaces/*.pyc")),
		("synthDrivers", glob("synthDrivers/*.py*")),
		("appModules", glob("appModules/*.py*")),
		("appModules", glob("appModules/*.kbd")),
		("lib", glob("lib/*")),
		("waves", glob("waves/*.wav")),
		("images", glob("images/*.png")),
	] + getLocaleDataFiles()+getUserDocsDataFiles(),
)
