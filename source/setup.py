# -*- coding: UTF-8 -*-
#setup.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Peter Vágner, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import sys
import copy
import gettext
gettext.install("nvda")
from setuptools import setup
import py2exe as py2exeModule
from glob import glob
import fnmatch
# versionInfo names must be imported after Gettext
# Suppress E402 (module level import not at top of file)
from versionInfo import (
	formatBuildVersionString,
	name,
	version,
	publisher
)  # noqa: E402
from versionInfo import *
from py2exe import distutils_buildexe
from py2exe.dllfinder import DllFinder
import wx
import importlib.machinery
# Explicitly put the nvda_dmp dir on the build path so the DMP library is included
sys.path.append(os.path.join("..", "include", "nvda_dmp"))
RT_MANIFEST = 24
manifest_template = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
	<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
		<security>
			<requestedPrivileges>
				<requestedExecutionLevel
					level="asInvoker"
					uiAccess="%(uiAccess)s"
				/>
			</requestedPrivileges>
		</security>
	</trustInfo>
	<compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
		<application>
			<!-- Windows 7 -->
			<supportedOS
				Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"
			/>
			<!-- Windows 8 -->
			<supportedOS
				Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"
			/>
			<!-- Windows 8.1 -->
			<supportedOS
				Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"
			/>
			<!-- Windows 10 -->
			<supportedOS
				Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"
			/>
		</application> 
	</compatibility>
</assembly>
"""

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

class py2exe(distutils_buildexe.py2exe):
	"""Overridden py2exe command to:
		* Add a command line option --enable-uiAccess to enable uiAccess for the main executable and EOA proxy
		* Add a manifest to the executables
	"""

	user_options = distutils_buildexe.py2exe.user_options + [
		("enable-uiAccess", "u", "enable uiAccess for the main executable"),
	]

	def initialize_options(self):
		super(py2exe, self).initialize_options()
		self.enable_uiAccess = False

	def run(self):
		dist = self.distribution
		if self.enable_uiAccess:
			# Add a target for nvda_uiAccess, using nvda_noUIAccess as a base.
			target = copy.deepcopy(dist.windows[0])
			target["dest_base"] = "nvda_uiAccess"
			target['uiAccess'] = True
			dist.windows.insert(1, target)
			# nvda_eoaProxy should have uiAccess.
			target = dist.windows[3]
			target['uiAccess'] = True
		# Add a manifest resource to every target at runtime.
		for target in dist.windows:
			target["other_resources"] = [
				(
					RT_MANIFEST,
					1,
					(manifest_template % dict(uiAccess=target['uiAccess'])).encode("utf-8")
				),
			]
		super(py2exe, self).run()

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
			"dest_base":"nvda_noUIAccess",
			"uiAccess": False,
			"icon_resources":[(1,"images/nvda.ico")],
			"other_resources": [], # Populated at run time
			"version":formatBuildVersionString(),
			"description":"NVDA application",
			"product_name":name,
			"product_version":version,
			"copyright":copyright,
			"company_name":publisher,
		},
		# The nvda_uiAccess target will be added at runtime if required.
		{
			"script": "nvda_slave.pyw",
			"uiAccess": False,
			"icon_resources": [(1,"images/nvda.ico")],
			"other_resources": [], # Populated at run time
			"version":formatBuildVersionString(),
			"description": name,
			"product_name":name,
			"product_version": version,
			"copyright": copyright,
			"company_name": publisher,
		},
		{
			"script": "nvda_eoaProxy.pyw",
			# uiAccess will be enabled at runtime if appropriate.
			"uiAccess": False,
			"icon_resources": [(1,"images/nvda.ico")],
			"other_resources": [], # Populated at run time
			"version":formatBuildVersionString(),
			"description": "NVDA Ease of Access proxy",
			"product_name":name,
			"product_version": version,
			"copyright": copyright,
			"company_name": publisher,
		},
	],
	console=[
		{
			"script": os.path.join("..", "include", "nvda_dmp", "nvda_dmp.py"),
			"uiAccess": False,
			"icon_resources": [(1, "images/nvda.ico")],
			"other_resources": [],  # Populated at runtime
			"version":formatBuildVersionString(),
			"description": "NVDA Diff-match-patch proxy",
			"product_name": name,
			"product_version": version,
			"copyright": f"{copyright}, Bill Dengler",
			"company_name": f"Bill Dengler, {publisher}",
		},
	],
	options = {"py2exe": {
		"bundle_files": 3,
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
	}},
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
		(".", ['message.html' ])
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
		+ getRecursiveDataFiles('documentation', '../user_docs', excludes=('*.t2t', '*.t2tconf', '*/developerGuide.*'))
	),
)
