# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Peter Vágner, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import argparse
import os
import sys
import gettext
gettext.install("nvda")
from glob import glob
import fnmatch
# versionInfo names must be imported after Gettext
# Suppress E402 (module level import not at top of file)
from versionInfo import (
	copyright as NVDAcopyright,  # copyright is a reserved python keyword
	description,
	formatBuildVersionString,
	name,
	publisher,
	version,
)  # noqa: E402
from py2exe import freeze  # noqa: E402
from py2exe.dllfinder import DllFinder  # noqa: E402
import wx
import importlib.machinery
# Explicitly put the nvda_dmp dir on the build path so the DMP library is included
sys.path.append(os.path.join("..", "include", "nvda_dmp"))
RT_MANIFEST = 24
manifestTemplateFilePath = "manifest.template.xml"

# py2exe's idea of whether a dll is a system dll appears to be wrong sometimes, so monkey patch it.
orig_determine_dll_type = DllFinder.determine_dll_type
def determine_dll_type(self, imagename):
	dll = os.path.basename(imagename).lower()
	if dll.startswith("api-ms-win-") or dll in ("powrprof.dll", "mpr.dll", "crypt32.dll"):
		# These are definitely system dlls available on all systems and must be excluded.
		# Including them can cause serious problems when a binary build is run on a different version of Windows.
		return None
	return orig_determine_dll_type(self, imagename)
DllFinder.determine_dll_type = determine_dll_type


def _parsePartialArguments() -> argparse.Namespace:
	"""
	Adds a command line option --enable-uiAccess to enable uiAccess for the main executable and EOA proxy
	Allows py2exe to parse the rest of the arguments
	"""
	partialParser = argparse.ArgumentParser()
	partialParser.add_argument(
		"--enable-uiAccess",
		dest="uiAccess",
		action="store_true",
		help="enable uiAccess for the main executable",
		default=False,
	)
	partialArgs, _argslist = partialParser.parse_known_args(sys.argv)
	return partialArgs


_partialArgs = _parsePartialArguments()


with open(manifestTemplateFilePath, "r", encoding="utf-8") as manifestTemplateFile:
	_manifestTemplate = manifestTemplateFile.read()


def getLocaleDataFiles():
	wxDir=wx.__path__[0]
	localeMoFiles=set()
	for f in glob("locale/*/LC_MESSAGES"):
		localeMoFiles.add((f, (os.path.join(f,"nvda.mo"),)))
		wxMoFile=os.path.join(wxDir,f,"wxstd.mo")
		if os.path.isfile(wxMoFile):
			localeMoFiles.add((f,(wxMoFile,))) 
		lang=os.path.split(os.path.split(f)[0])[1]
		if '_' in lang:
				lang=lang.split('_')[0]
				f=os.path.join('locale',lang,'lc_messages')
				wxMoFile=os.path.join(wxDir,f,"wxstd.mo")
				if os.path.isfile(wxMoFile):
					localeMoFiles.add((f,(wxMoFile,))) 
	localeDicFiles=[(os.path.dirname(f), (f,)) for f in glob("locale/*/*.dic")]
	NVDALocaleGestureMaps=[(os.path.dirname(f), (f,)) for f in glob("locale/*/gestures.ini")]
	return list(localeMoFiles)+localeDicFiles+NVDALocaleGestureMaps

def getRecursiveDataFiles(dest,source,excludes=()):
	rulesList=[]
	rulesList.append((dest,
		[f for f in glob("%s/*"%source) if not any(fnmatch.fnmatch(f,exclude) for exclude in excludes) and os.path.isfile(f)]))
	[rulesList.extend(getRecursiveDataFiles(os.path.join(dest,dirName),os.path.join(source,dirName),excludes=excludes)) for dirName in os.listdir(source) if os.path.isdir(os.path.join(source,dirName)) and not dirName.startswith('.')]
	return rulesList


def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
	return (
		RT_MANIFEST,
		1,
		(_manifestTemplate % {"uiAccess": shouldHaveUIAccess}).encode("utf-8")
	)


_py2ExeWindows = [
	{
		"script": "nvda.pyw",
		"dest_base": "nvda_noUIAccess",
		"icon_resources": [(1, "images/nvda.ico")],
		"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
		"version_info": {
			"version": formatBuildVersionString(),
			"description": "NVDA application (no UIAccess)",
			"product_name": name,
			"product_version": version,
			"copyright": NVDAcopyright,
			"company_name": publisher,
		}
	},
	# The nvda_uiAccess target will be added at runtime if required.
	{
		"script": "nvda_slave.pyw",
		"icon_resources": [(1, "images/nvda.ico")],
		"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
		"version_info": {
			"version": formatBuildVersionString(),
			"description": description,
			"product_name": name,
			"product_version": version,
			"copyright": NVDAcopyright,
			"company_name": publisher,
		}
	},
]
if _partialArgs.uiAccess:
	_py2ExeWindows.insert(1, {
		"script": "nvda.pyw",
		"dest_base": "nvda_uiAccess",
		"icon_resources": [(1, "images/nvda.ico")],
		"other_resources": [_genManifestTemplate(shouldHaveUIAccess=True)],
		"version_info": {
			"version": formatBuildVersionString(),
			"description": "NVDA application (has UIAccess)",
			"product_name": name,
			"product_version": version,
			"copyright": NVDAcopyright,
			"company_name": publisher,
		}
	})


freeze(
	version_info={
		"version": formatBuildVersionString(),
		"description": description,
		"product_name": name,
		"product_version": version,
		"copyright": NVDAcopyright,
		"company_name": publisher,
	},
	windows=_py2ExeWindows,
	console=[
		{
			"script": os.path.join("..", "include", "nvda_dmp", "nvda_dmp.py"),
			"icon_resources": [(1, "images/nvda.ico")],
			"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
			"version_info": {
				"version": formatBuildVersionString(),
				"description": "NVDA Diff-match-patch proxy",
				"product_name": name,
				"product_version": version,
				"copyright": f"{NVDAcopyright}, Bill Dengler",
				"company_name": f"Bill Dengler, {publisher}",
			},
		},
	],
	options={
		"verbose": 2,
		"optimize": 0,
		"bundle_files": 3,
		"dist_dir": "../dist",
		"excludes": [
			"tkinter",
			"serial.loopback_connection",
			"serial.rfc2217",
			"serial.serialcli",
			"serial.serialjava",
			"serial.serialposix",
			"serial.socket_connection",
			# netbios (from pywin32) is optionally used by Python3's uuid module.
			# This is not needed.
			# We also need to exclude win32wnet explicitly.
			"netbios",
			"win32wnet",
			# winxptheme is optionally used by wx.lib.agw.aui.
			# We don't need this.
			"winxptheme",
			# numpy is an optional dependency of comtypes but we don't require it.
			"numpy",
			# multiprocessing isn't going to work in a frozen environment
			"multiprocessing",
			"concurrent.futures.process",
		],
		"packages": [
			"NVDAObjects",
			# As of py2exe 0.11.0.0 if the forcibly included package contains subpackages
			# they need to be listed explicitly (py2exe issue 113).
			"NVDAObjects.IAccessible",
			"NVDAObjects.JAB",
			"NVDAObjects.UIA",
			"NVDAObjects.window",
			"virtualBuffers",
			"appModules",
			"comInterfaces",
			"brailleDisplayDrivers",
			"brailleDisplayDrivers.albatross",
			"brailleDisplayDrivers.eurobraille",
			"synthDrivers",
			"visionEnhancementProviders",
		],
		"includes": [
			"nvdaBuiltin",
			# #3368: bisect was implicitly included with Python 2.7.3, but isn't with 2.7.5.
			"bisect",
			# robotremoteserver (for system tests) depends on xmlrpc.server
			"xmlrpc.server",
		],
	},
	data_files=[
		(".",glob("*.dll")+glob("*.manifest")+["builtin.dic"]),
		("documentation", ['../copying.txt', '../contributors.txt']),
		("lib/%s" % version, glob("lib/*.dll") + glob("lib/*.manifest")),
		("lib64/%s"%version, glob("lib64/*.dll") + glob("lib64/*.exe")),
		("libArm64/%s"%version, glob("libArm64/*.dll") + glob("libArm64/*.exe")),
		("waves", glob("waves/*.wav")),
		("images", glob("images/*.ico")),
		("fonts", glob("fonts/*.ttf")),
		("louis/tables",glob("louis/tables/*")),
		("COMRegistrationFixes", glob("COMRegistrationFixes/*.reg")),
		(".", glob("../miscDeps/python/*.dll")),
		(".", ['message.html']),
		(".", [os.path.join(sys.base_prefix, "python3.dll")]),
	] + (
		getLocaleDataFiles()
		+ getRecursiveDataFiles("synthDrivers", "synthDrivers",
			excludes=tuple(
				"*%s" % ext
				for ext in importlib.machinery.SOURCE_SUFFIXES + importlib.machinery.BYTECODE_SUFFIXES
			) + (
				"*.exp",
				"*.lib",
				"*.pdb",
				"__pycache__"
		))
		+ getRecursiveDataFiles("brailleDisplayDrivers", "brailleDisplayDrivers",
			excludes=tuple(
				"*%s" % ext
				for ext in importlib.machinery.SOURCE_SUFFIXES + importlib.machinery.BYTECODE_SUFFIXES
			) + (
				"__pycache__",
		))
	+ getRecursiveDataFiles(
		"documentation",
		"../user_docs",
		excludes=tuple(
			f"*{ext}" for ext in importlib.machinery.SOURCE_SUFFIXES + importlib.machinery.BYTECODE_SUFFIXES
			) + (
		"__pycache__",
		"*.t2t",
		"*.t2tconf",
		"*.md",
		"*/user_docs/styles.css",
		"*/developerGuide.*"
		)
	)
	),
)
