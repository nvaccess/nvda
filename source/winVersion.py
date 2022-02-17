# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Bill Dengler, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""A module used to record Windows versions.
It is also used to define feature checks such as
making sure NVDA can run on a minimum supported version of Windows.
"""

from typing import Optional
import sys
import os
import functools
import winreg


# Records a mapping between Windows builds and release names.
# These include build 10240 for Windows 10 1507 and releases with multiple release builds.
# These are applicable to Windows 10 and later as they report the same system version (10.0).
_BUILDS_TO_RELEASE_NAMES = {
	10240: "Windows 10 1507",
	10586: "Windows 10 1511",
	14393: "Windows 10 1607",
	15063: "Windows 10 1703",
	16299: "Windows 10 1709",
	17134: "Windows 10 1803",
	17763: "Windows 10 1809",
	18362: "Windows 10 1903",
	18363: "Windows 10 1909",
	19041: "Windows 10 2004",
	19042: "Windows 10 20H2",
	19043: "Windows 10 21H1",
	19044: "Windows 10 21H2",
	20348: "Windows Server 2022",
	22000: "Windows 11 21H2",
}


@functools.lru_cache(maxsize=1)
def _getRunningVersionNameFromWinReg() -> str:
	"""Returns the Windows release name defined in Windows Registry.
	This is applicable on Windows 10 Version 1511 (build 10586) and later.
	"""
	# Cache the version in use on the system.
	with winreg.OpenKey(
		winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion"
	) as currentVersion:
		# Version 20H2 and later where a separate display version string is used.
		try:
			releaseId = winreg.QueryValueEx(currentVersion, "DisplayVersion")[0]
		except OSError:
			# Don't set anything if this is Windows 10 1507 or earlier.
			try:
				releaseId = winreg.QueryValueEx(currentVersion, "ReleaseID")[0]
			except OSError:
				raise RuntimeError(
					"Release name is not recorded in Windows Registry on this version of Windows"
				) from None
	return releaseId


@functools.total_ordering
class WinVersion(object):
	"""
	Represents a Windows release.
	Includes version major, minor, build, service pack information,
	as well as tools such as checking for specific Windows 10 releases.
	"""

	def __init__(
			self,
			major: int = 0,
			minor: int = 0,
			build: int = 0,
			releaseName: Optional[str] = None,
			servicePack: str = "",
			productType: str = ""
	):
		self.major = major
		self.minor = minor
		self.build = build
		if releaseName:
			self.releaseName = releaseName
		else:
			self.releaseName = self._getWindowsReleaseName()
		self.servicePack = servicePack
		self.productType = productType

	def _getWindowsReleaseName(self) -> str:
		"""Returns the public release name for a given Windows release based on major, minor, and build.
		This is useful if release names are not defined when constructing this class.
		For example, 6.1 will return 'Windows 7'.
		For Windows 10, feature update release name will be included.
		On server systems, unless noted otherwise, client release names will be returned.
		For example, 'Windows 10 1809' will be returned on Server 2019 systems.
		"""
		if (self.major, self.minor) == (6, 1):
			return "Windows 7"
		elif (self.major, self.minor) == (6, 2):
			return "Windows 8"
		elif (self.major, self.minor) == (6, 3):
			return "Windows 8.1"
		elif self.major == 10:
			# From Version 1511 (build 10586), release Id/display version comes from Windows Registry.
			# However there are builds with no release name (Version 1507/10240)
			# or releases with different builds.
			# Look these up first before asking Windows Registry.
			if self.build in _BUILDS_TO_RELEASE_NAMES:
				return _BUILDS_TO_RELEASE_NAMES[self.build]
			return "Windows 10 unknown"
		else:
			return "Windows release unknown"

	def __repr__(self):
		winVersionText = [self.releaseName]
		winVersionText.append(f"({self.major}.{self.minor}.{self.build})")
		if self.servicePack != "":
			winVersionText.append(f"service pack {self.servicePack}")
		if self.productType != "":
			winVersionText.append(self.productType)
		return " ".join(winVersionText)

	def __eq__(self, other):
		return (
			(self.major, self.minor, self.build)
			== (other.major, other.minor, other.build)
		)

	def __ge__(self, other):
		return (
			(self.major, self.minor, self.build)
			>= (other.major, other.minor, other.build)
		)


# Windows releases to WinVersion instances for easing comparisons.
WIN7 = WinVersion(major=6, minor=1, build=7600)
WIN7_SP1 = WinVersion(major=6, minor=1, build=7601, servicePack="1")
WIN8 = WinVersion(major=6, minor=2, build=9200)
WIN81 = WinVersion(major=6, minor=3, build=9600)
WIN10 = WIN10_1507 = WinVersion(major=10, minor=0, build=10240)
WIN10_1511 = WinVersion(major=10, minor=0, build=10586)
WIN10_1607 = WinVersion(major=10, minor=0, build=14393)
WIN10_1703 = WinVersion(major=10, minor=0, build=15063)
WIN10_1709 = WinVersion(major=10, minor=0, build=16299)
WIN10_1803 = WinVersion(major=10, minor=0, build=17134)
WIN10_1809 = WinVersion(major=10, minor=0, build=17763)
WIN10_1903 = WinVersion(major=10, minor=0, build=18362)
WIN10_1909 = WinVersion(major=10, minor=0, build=18363)
WIN10_2004 = WinVersion(major=10, minor=0, build=19041)
WIN10_20H2 = WinVersion(major=10, minor=0, build=19042)
WIN10_21H1 = WinVersion(major=10, minor=0, build=19043)
WIN10_21H2 = WinVersion(major=10, minor=0, build=19044)
WINSERVER_2022 = WinVersion(major=10, minor=0, build=20348)
WIN11 = WIN11_21H2 = WinVersion(major=10, minor=0, build=22000)


@functools.lru_cache(maxsize=1)
def getWinVer():
	"""Returns a record of current Windows version NVDA is running on.
	"""
	winVer = sys.getwindowsversion()
	# #12509: on Windows 10, fetch whatever Windows Registry says for the current build.
	# #12626: note that not all Windows 10 releases are labeled "Windows 10"
	# (build 22000 is Windows 11 despite major.minor being 10.0).
	try:
		if WinVersion(
			major=winVer.major,
			minor=winVer.minor,
			build=winVer.build
		) >= WIN11:
			releaseName = f"Windows 11 {_getRunningVersionNameFromWinReg()}"
		else:
			releaseName = f"Windows 10 {_getRunningVersionNameFromWinReg()}"
	except RuntimeError:
		releaseName = None
	return WinVersion(
		major=winVer.major,
		minor=winVer.minor,
		build=winVer.build,
		releaseName=releaseName,
		servicePack=winVer.service_pack,
		productType=("workstation", "domain controller", "server")[winVer.product_type - 1]
	)


def isSupportedOS():
	# NVDA can only run on Windows 7 Service pack 1 and above
	return getWinVer() >= WIN7_SP1


UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")


def isUwpOcrAvailable():
	return os.path.isdir(UWP_OCR_DATA_PATH)


def isFullScreenMagnificationAvailable() -> bool:
	"""
	Technically this is always False. The Magnification API has been marked by MS as unsupported for
	WOW64 applications such as NVDA. For our usages, support has been added since Windows 8, relying on our
	testing our specific usage of the API with each Windows version since Windows 8
	"""
	return getWinVer() >= WIN8
