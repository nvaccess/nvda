# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2025 NV Access Limited, Luke Davis (Open Source Systems, Ltd.)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities to re-register  particular system COM interfaces needed by NVDA.
Relevant discussions of DLLs, registry keys, and paths, can be found on these issues:
https://github.com/nvaccess/nvda/issues/2807#issuecomment-320149243
https://github.com/nvaccess/nvda/issues/9039
https://github.com/nvaccess/nvda/issues/12560
"""

import os
import subprocess
import sysconfig
import winVersion
import globalVars
from logHandler import log

OLEACC_REG_FILE_PATH = os.path.join(globalVars.appDir, "COMRegistrationFixes", "oleaccProxy.reg")
# Particular  64 bit / 32 bit system paths
SYSTEM_ROOT = os.path.expandvars("%SYSTEMROOT%")
SYSTEM32 = os.path.join(SYSTEM_ROOT, "System32")
SYSNATIVE = os.path.join(SYSTEM_ROOT, "Sysnative")  # Virtual folder for reaching 64-bit exes from 32-bit apps
SYSTEM_DRIVE = os.path.expandvars("%SYSTEMDRIVE%\\")
PROGRAM_FILES = os.path.join(SYSTEM_DRIVE, "Program Files")
PROGRAM_FILES_X86 = os.path.join(SYSTEM_DRIVE, "Program Files (x86)")


def register32bitServer(fileName: str) -> None:
	"""Registers the COM proxy dll with the given file name, using the 32-bit version of regsvr32.

	:param fileName: The 32 bit path to the DLL
	"""
	if sysconfig.get_platform() == "win32":
		# NVDA is 32 bit.
		# On 32-bit systems, the 32-bit version of regsvr32.exe is in System32.
		# On 64-bit systems, the 32-bit version of regsvr32.exe is in SysWOW64,
		# but system32 is automatically redirected to SysWOW64 for 32-bit applications.
		regsvr32 = os.path.join(SYSTEM_ROOT, "system32", "regsvr32.exe")
	else:
		# NVDA is 64 bit, and therefore the OS is also 64 bit.
		# On 64-bit systems, the 32-bit version of regsvr32.exe is in SysWOW64.
		regsvr32 = os.path.join(SYSTEM_ROOT, "SysWOW64", "regsvr32.exe")
	# Make sure a console window doesn't show when running regsvr32.exe
	startupInfo = subprocess.STARTUPINFO()
	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	startupInfo.wShowWindow = subprocess.SW_HIDE
	try:
		subprocess.check_call([regsvr32, "/s", fileName], startupinfo=startupInfo)
	except subprocess.CalledProcessError as e:
		log.error(f"Error registering {fileName} in a 32-bit context: {e}")
	else:
		log.debug(f"Registered {fileName} in a 32-bit context.")


def register64bitServer(fileName: str) -> None:
	"""Registers the COM proxy dll with the given file name, using the 64-bit version of regsvr64.

	:param fileName: The 64 bit path to the DLL
	"""
	if sysconfig.get_platform() == "win32":
		# NVDA is 32 bit.
		# On 64 bit systems, Sysnative provides a virtual directory to reach 64-bit executables from 32-bit applications.
		regsvr32 = os.path.join(SYSTEM_ROOT, "Sysnative", "regsvr32.exe")
	else:
		# NVDA is 64 bit.
		# On 64-bit systems, the 64-bit version of regsvr32.exe is in System32.
		regsvr32 = os.path.join(SYSTEM_ROOT, "system32", "regsvr32.exe")
	# Make sure a console window doesn't show when running regsvr32.exe
	startupInfo = subprocess.STARTUPINFO()
	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	startupInfo.wShowWindow = subprocess.SW_HIDE
	try:
		subprocess.check_call([regsvr32, "/s", fileName], startupinfo=startupInfo)
	except subprocess.CalledProcessError as e:
		log.error(f"Error registering {fileName} in a 64-bit context: {e}")
	else:
		log.debug(f"Registered {fileName} in a 64-bit context.")


def apply32bitRegistryPatch(fileName: str) -> None:
	"""Applies the registry patch with the given file name, using 32-bit regExe.

	:param fileName: The 32 bit path to the .reg file
	"""
	if not os.path.isfile(fileName):
		raise FileNotFoundError(f"Cannot apply 32-bit registry patch: {fileName} not found.")
	if sysconfig.get_platform() == "win32":
		# NVDA is 32 bit.
		# On 32-bit systems, the 32-bit version of reg.exe is in System32.
		# On 64-bit systems, the 32-bit version of reg.exe is in SysWOW64,
		# but system32 is automatically redirected to SysWOW64 for 32-bit applications.
		regExe = os.path.join(SYSTEM_ROOT, "System32", "reg.exe")
	else:
		# NVDA is 64 bit, and therefore the OS is also 64 bit.
		# On 64-bit systems, the 32-bit version of reg.exe is in SysWOW64.
		regExe = os.path.join(SYSTEM_ROOT, "SysWOW64", "reg.exe")
	# Make sure a console window doesn't show when running reg.exe
	startupInfo = subprocess.STARTUPINFO()
	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	startupInfo.wShowWindow = subprocess.SW_HIDE
	try:
		subprocess.check_call([regExe, "import", fileName], startupinfo=startupInfo)
	except subprocess.CalledProcessError as e:
		log.error(f"Error applying 32-bit registry patch from {fileName} with {regExe}: {e}")
	else:
		log.debug(f"Applied 32-bit registry patch from {fileName}")


def apply64bitRegistryPatch(fileName: str) -> None:
	"""Applies the registry patch with the given file name, using 64-bit regExe.

	:param fileName: The 64 bit path to the .reg file
	"""
	if not os.path.isfile(fileName):
		raise FileNotFoundError(f"Cannot apply 64-bit registry patch: {fileName} not found.")
	if sysconfig.get_platform() == "win32":
		# NVDA is 32 bit.
		# On 64-bit systems, Sysnative provides a virtual directory to reach 64-bit executables from 32-bit applications.
		regExe = os.path.join(SYSTEM_ROOT, "Sysnative", "reg.exe")
	else:
		# NVDA is 64 bit.
		# On 64-bit systems, the 64-bit version of reg.exe is in System32.
		regExe = os.path.join(SYSTEM_ROOT, "system32", "reg.exe")
	# Make sure a console window doesn't show when running reg.exe
	startupInfo = subprocess.STARTUPINFO()
	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	startupInfo.wShowWindow = subprocess.SW_HIDE
	try:
		subprocess.check_call([regExe, "import", fileName], startupinfo=startupInfo)
	except subprocess.CalledProcessError as e:
		log.error(f"Error applying 64-bit registry patch from {fileName} with {regExe}: {e}")
	else:
		log.debug(f"Applied 64-bit registry patch from {fileName}")


def fixCOMRegistrations() -> None:
	"""Registers most common COM proxies, in case they have accidentally been unregistered or overwritten by
	3rd party software installs or uninstalls.
	"""
	winVer = winVersion.getWinVer()
	OSMajorMinor = (winVer.major, winVer.minor)
	is64bit = winVer.processorArchitecture.endswith("64")
	log.debug(
		f"Fixing COM registrations for Windows {OSMajorMinor[0]}.{OSMajorMinor[1]}, {{}} bit.".format(
			"64" if is64bit else "32",
		),
	)
	# OLEACC (MSAA) proxies
	apply32bitRegistryPatch(OLEACC_REG_FILE_PATH)
	if is64bit:
		apply64bitRegistryPatch(OLEACC_REG_FILE_PATH)
	# IDispatch and other common OLE interfaces
	register32bitServer(os.path.join(SYSTEM32, "oleaut32.dll"))
	register32bitServer(os.path.join(SYSTEM32, "actxprxy.dll"))
	if is64bit:
		register64bitServer(os.path.join(SYSTEM32, "oleaut32.dll"))
		register64bitServer(os.path.join(SYSTEM32, "actxprxy.dll"))
