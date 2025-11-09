# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from glob import glob
import sys
sys.path.insert(0, '../source')

import gettext
from buildVersion import (
	formatBuildVersionString,
	name,
	publisher,
	version,
)

gettext.install("nvda")

# versionInfo names must be imported after Gettext
# Suppress E402 (module level import not at top of file)
from versionInfo import (  # noqa: E402
	copyright as NVDAcopyright,  # copyright is a reserved python keyword
	description,
)
from py2exe import freeze  # noqa: E402
from py2exe.dllfinder import DllFinder  # noqa: E402

RT_MANIFEST = 24
manifestTemplateFilePath = "../source/manifest.template.xml"

with open(manifestTemplateFilePath, "r", encoding="utf-8") as manifestTemplateFile:
	_manifestTemplate = manifestTemplateFile.read()

def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
	return (
		RT_MANIFEST,
		1,
		(_manifestTemplate % {"uiAccess": shouldHaveUIAccess}).encode("utf-8"),
	)

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


freeze(
	version_info={
		"version": formatBuildVersionString(),
		"description": description,
		"product_name": name,
		"product_version": version,
		"copyright": NVDAcopyright,
		"company_name": publisher,
	},
	console=[
		{
			"script": "../source/nvda_art.pyw",
			"dest_base": "nvda_art",
			"icon_resources": [(1, "../source/images/nvda.ico")],
			"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
			"version_info": {
				"version": formatBuildVersionString(),
				"description": "NVDA Add-on Runtime",
				"product_name": "NVDA ART",
				"product_version": version,
				"copyright": NVDAcopyright,
				"company_name": publisher,
			},
		},
	],
	options={
		"verbose": 2,
		# Removes assertions for builds.
		# https://docs.python.org/3.13/tutorial/modules.html#compiled-python-files
		"optimize": 1,
		"bundle_files": 3,
		"dist_dir": "../source/lib/x86/art-runtime",
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
			# multiprocessing isn't going to work in a frozen environment
			"multiprocessing",
			"concurrent.futures.process",
			# Tomli is part of Python 3.11+ as Tomlib, but is imported as tomli by cryptography, which causes an infinite loop in py2exe
			"tomli",
		],
		"packages": [
			"comInterfaces",
			# ART dependencies
			"art",
			"Pyro5",
		],
		"includes": [
			# #3368: bisect was implicitly included with Python 2.7.3, but isn't with 2.7.5.
			"bisect",
		],
	},
	data_files=[
		(".", glob("*.dll") + glob("*.manifest")),
	]
)
