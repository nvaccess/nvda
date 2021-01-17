# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities to re-register  particular system COM interfaces needed by NVDA."""

import os
import subprocess
import winVersion
import globalVars
from logHandler import log

# Particular  64 bit / 32 bit system paths
systemRoot=os.path.expandvars('%SYSTEMROOT%')
system32=os.path.join(systemRoot,'system32')
sysWow64=os.path.join(systemRoot,'syswow64')
systemDrive=os.path.expandvars('%SYSTEMDRIVE%\\')
programFiles=os.path.join(systemDrive,'program files')
programFilesX86=os.path.join(systemDrive,'program files (x86)')

def registerServer(fileName,wow64=False):
	"""
	Registers the COM proxy dll with the given file name
	Using regsvr32.
	@param fileName: the path to the dll
	@type fileName: str
	@param wow64: If true then the 32 bit (wow64) version of regsvr32 will be used.
	@type wow64: bool
	"""
	regsvr32=os.path.join(sysWow64 if wow64 else system32,'regsvr32.exe')
	try:
		subprocess.check_call([regsvr32,'/s',fileName])
	except subprocess.CalledProcessError as e:
		log.error("Error registering %s, %s"%(fileName,e))
	else:
		log.debug("Registered %s"%fileName)

def applyRegistryPatch(fileName,wow64=False):
	"""
	Applies the registry patch with the given file name
	using regedit.
	@param fileName: the path to the .reg file
	@type fileName: str
	"""
	if not os.path.isfile(fileName):
		raise FileNotFoundError(f"Cannot apply registry patch, {fileName} not found.")
	regedit=os.path.join(sysWow64 if wow64 else systemRoot,'regedit.exe')
	try:
		subprocess.check_call([regedit,'/s',fileName])
	except subprocess.CalledProcessError as e:
		log.error("Error applying registry patch: %s with %s, %s"%(fileName,regedit,e))
	else:
		log.debug("Applied registry patch: %s with %s"%(fileName,regedit))


OLEACC_REG_FILE_PATH = os.path.join(globalVars.appDir, "COMRegistrationFixes", "oleaccProxy.reg")
def fixCOMRegistrations():
	"""
	Registers most common COM proxies, in case they had accidentally been unregistered or overwritten by 3rd party software installs/uninstalls.
	"""
	is64bit=os.environ.get("PROCESSOR_ARCHITEW6432","").endswith('64')
	OSMajorMinor=winVersion.winVersion[:2]
	log.debug("Fixing COM registration for Windows %s.%s, %s"%(OSMajorMinor[0],OSMajorMinor[1],"64 bit" if is64bit else "32 bit"))  
	# Commands taken from NVDA issue #2807 comment https://github.com/nvaccess/nvda/issues/2807#issuecomment-320149243
	# OLEACC (MSAA) proxies
	applyRegistryPatch(OLEACC_REG_FILE_PATH)
	if is64bit:
		applyRegistryPatch(OLEACC_REG_FILE_PATH, wow64=True)
	# IDispatch and other common OLE interfaces
	registerServer(os.path.join(system32,'oleaut32.dll'))
	registerServer(os.path.join(system32,'actxprxy.dll'))
	if is64bit:
		registerServer(os.path.join(sysWow64,'oleaut32.dll'),wow64=True)
		registerServer(os.path.join(sysWow64,'actxprxy.dll'),wow64=True)
	# IServiceProvider on windows 7 can become unregistered 
	if OSMajorMinor==(6,1): # Windows 7
		registerServer(os.path.join(programFiles,'Internet Explorer','ieproxy.dll'))
		if is64bit:
			registerServer(os.path.join(programFilesX86,'Internet Explorer','ieproxy.dll'),wow64=True)
