# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import importlib
import fnmatch
from glob import glob
import sys

nvdaSourceDir = "../../source"
runtimeSourceDir = "../../source/_bridge/runtimes/synthDriverHost"
runtimeName = "synthDriverHost"
runtimeDestDir = f"{nvdaSourceDir}/lib/x86/synthDriverHost-runtime"


sys.path.insert(0, nvdaSourceDir)

import gettext
from buildVersionLoader import (
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
manifestTemplateFilePath = f"{nvdaSourceDir}/manifest.template.xml"

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

def getRecursiveDataFiles(dest: str, source: str, excludes: tuple = ()) -> list[tuple[str, list[str]]]:
	rulesList: list[tuple[str, list[str]]] = []
	for file in glob(f"{source}/*"):
		if not any(fnmatch.fnmatch(file, exclude) for exclude in excludes) and os.path.isfile(file):
			rulesList.append((dest, [file]))
	for dirName in os.listdir(source):
		if os.path.isdir(os.path.join(source, dirName)) and not dirName.startswith("."):
			rulesList.extend(
				getRecursiveDataFiles(
					os.path.join(dest, dirName),
					os.path.join(source, dirName),
					excludes=excludes,
				),
			)
	return rulesList

sys.path.insert(0, runtimeSourceDir)

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
			"script": f"{runtimeSourceDir}/main.pyw",
			"dest_base": f"nvda_{runtimeName}",
			"icon_resources": [(1, f"{nvdaSourceDir}/images/nvda.ico")],
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
		"dist_dir": runtimeDestDir,
		"excludes": [
			"_localCaptioner",
			"_remoteClient",
			"addonHandler",
			"addonStore",
			"appModules",
			"audio",
			"brailleDisplayDrivers",
			"brailleTables",
			"COMRegistrationFixes",
			"documentNavigation",
			"contentRegoc",
			"controlTypes",
			"globalPlugins",
			"gui",
			"hwIo",
			"IAccessibleHandler",
			"louis",
			"mathPres",
			"monkeyPatches",
			"NVDAHelper",
			"NVDAObjects",
			"screenCurtain",
			"textInfos",
			"textUtils",
			"UIAHandler",
			"virtualBuffers",
			"vision",
			"visionEnhancementProviders",
			"wx",
			"addonAPIVersion",
			"annotation",
			"api",
			"appModuleHandler",
			"aria",
			"bdDetect",
			"braille",
			"brailleInput",
			"browseMode",
			"characterProcessing",
			"compoundDocuments",
			"core",
			"cursorManager",
			"diffHandler",
			"displayModel",
			"documentBase",
			"easeOfAccess",
			"editableText",
			"eventHandler",
			"globalCommands",
			"globalPluginHandler",
			"hwPortUtils",
			"inputCore",
			"installer",
			"JABHandler",
			"keyboardHandler",
			"keyLabels",
			"locationHelper",
			"louisHelper",
			"mathType",
			"mouseHandler",
			"oleacc",
			"pythonConsole",
			"queueHandler",
			"review",
			"screenBitmap",
			"screenExplorer",
			"scriptHandler",
			"speechViewer",
			"tableUtils",
			"tones",
			"touchhandler",
			"touchTracker",
			"treeInterceptorHandler",
			"ui",
			"updateCheck",
			"vkCodes",
			"watchdog",
			"wincon",
			"winConsoleHandler",
			"windowUtils",
			
			"winInputHook",
			"xmlFormatting",
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
			"synthDrivers",
		],
		"includes": [
			# #3368: bisect was implicitly included with Python 2.7.3, but isn't with 2.7.5.
			"bisect",
			"win32event",
			"win32file",
			"win32pipe",
			"audioDucking",
			"comtypes.stream",
		],
	},
	data_files=[
		(".", glob("*.dll") + glob("*.manifest")),
	] + getRecursiveDataFiles(
		"synthDrivers",
		f"{runtimeSourceDir}\\synthDrivers",
		excludes=tuple(f"*{ext}" for ext in importlib.machinery.all_suffixes())
		+ (
			"*.exp",
			"*.lib",
			"*.pdb",
		),
	)
)
